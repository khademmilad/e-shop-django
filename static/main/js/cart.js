$('.addToCartBtn').click(function (e){
    e.preventDefault();

    let product_id = $(this).closest('.product_data').find('.prodt_id').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
       method: "POST",
       url: "/product/add-to-cart/",
       data: {
          'product_id': product_id,
          csrfmiddlewaretoken: token
       },
       dataType: "dataType",
       success: function (response) {
          console.log(response);
          location.reload();
       }
    })
       
 });
 