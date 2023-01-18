import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from product.models import Cart, Order, OrderItem
from product.models import Payment



def go_to_gateway_view(request):

    # خواندن مبلغ از هر جایی که مد نظر است

    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    if cart_items:
        for item in cart_items:
            total_price += (item.product.price) * item.quantity

    amount = total_price

    print('amount', amount)

    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url('/callback-gateway')
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()


        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e



def callback_gateway_view(request):

    current_user = request.user

    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404
    
    print('bank_record', bank_record.__dict__)

    # to create payment object
    new_payment = Payment()
    new_payment.user = current_user
    new_payment.payment_number = bank_record.tracking_code
    new_payment.payment_method = bank_record.bank_type
    new_payment.amount_paid = bank_record.amount
    new_payment.status = bank_record.status
    new_payment.save()

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.

        # to get the total price of items in cart
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0
        if cart_items:
            for item in cart_items:
                total_price += (item.product.price) * item.quantity


        # to create order object
        new_order = Order()
        new_order.user = current_user
        new_order.payment = new_payment
        new_order.total_price = total_price
        new_order.tracking_code = bank_record.tracking_code
        new_order.save()

        # to create order items from cart's item
        new_order_item = Cart.objects.filter(user=current_user)
        for item in new_order_item:
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity
            )

        # to clear user's cart
        Cart.objects.filter(user=current_user).delete()

        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # if payment was failure
    else:
        # to clear user's cart
        Cart.objects.filter(user=current_user).delete()

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")