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
       success: function (response) {
        location.reload(); 
       }
    })
    
 });
 

let updateBtns = document.getElementsByClassName('update-cart')
let token = $('input[name=csrfmiddlewaretoken]').val();

for (i = 0; i < updateBtns.length; i++) {
   updateBtns[i].addEventListener('click', function(){
      let productId = this.dataset.product
      let action = this.dataset.action
      console.log('productId', productId, 'action', action)

      updateQuantity(productId, action);
   })
}

function updateQuantity(productId, action){

   let url = '/product/update-cart/'

   fetch(url, {
      method: "POST",
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': token,
      },
      body:JSON.stringify({'productId':productId, 'action': action})
   })

   .then((response) => {
      return response.json();
   })

   .then((data) => {
      console.log('data:', data);
      location.reload();
})
   
}