'use strict';

const createOutfitButton = document.querySelector("#generate_outfit");
createOutfitButton.addEventListener('click', handleClick);
const generateAnotherOutfitButton = document.querySelector('input#generate-other-outfit-button');
generateAnotherOutfitButton.addEventListener('click', handleClick);

function handleClick(evt) {
    evt.preventDefault();
    
    const formInputs = {
        occasion: document.querySelector('#user_occasion').value,
        season: document.querySelector('#current_season').value,
        color: document.querySelector('#add-color').value,
        wantHat: document.querySelector('#user_wants_hat').checked,
        wantBag: document.querySelector('#user_wants_bags').checked,
        wantGlasses: document.querySelector('#user_wants_glasses').checked,
        typeOfOutfit:  document.querySelector('#type-outfit').value,
        title: document.querySelector('#outfit_title').value
    };
    
    fetch('/view_outfit', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        // clear out the previous options if any
        document.querySelector('#outfit-viewer').innerHTML = '';
        
        if (responseJson.length === 0) {
            alert("No items in your closet that matches this search. Try again.");
        };
        
        responseJson.forEach(([item, data]) => {
            document.querySelector('#outfit-viewer').insertAdjacentHTML(
                'beforeend', 
                `<div><img
                data-id=${data.id} 
                width=200px; 
                display: inline-block; 
                src="${data.url}"/></div>`
                );
            });
            
            document.querySelector('input#generate-other-outfit-button').style.display = "block";
            // // If you want to remove the form when results are shown
            // document.querySelector('#create-outfit-form').style.display = 'none';
            document.querySelector('#outfit-viewer').insertAdjacentHTML(
                'beforebegin',
                '<form id="favorite-outfit" action="/favorites" method="POST"><button value="Favorite" id="favorite-outfit-button"> Favorite </button></form>'
                );
            const favoriteOutfitButton = document.querySelector('#favorite-outfit-button');
            favoriteOutfitButton.addEventListener('click', (evt) => {
                evt.preventDefault();
    
                const imgElements = document.getElementById("outfit-viewer");
                let listImgs = {};

                listImgs[0] = imgElements.firstChild.firstChild.getAttribute('data-id');

                })
                fetch('/favorite-elements', {
                    method: 'POST',
                    body: JSON.stringify(listImgs),
                    headers: {
                        'Content-type': 'application/json',
                    },
                })
                .then((response) => response.json())
                .then((responseImgs) => {
                    alert("Successfully added to your favs!");
                });
        });
        };