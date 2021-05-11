console.log("user:",user)

var updatebtns = document.getElementsByClassName('add_cart')

for(i = 0; i<updatebtns.length; i++){
	updatebtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action

		if(user == "AnonymousUser"){
			console.log('Not authenticated');
		}
		else{
			updateUserOrder(productId, action)

		}
	})
}

function updateUserOrder(productID, action){
	console.log('authenticated');
	var url = '/updatecart/'
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		
		body: JSON.stringify({
			'productID': productID,
			'action':action
		})
	})

	.then((response) => {
		return response.json()
	})

	.then((data) => {
		location.reload()
	})
}