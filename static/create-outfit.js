'use strict';

const createOutfitButton = document.querySelector("#generate_outfit");
createOutfitButton.addEventListener('click', handleClick);


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
        createOutfitButton.innerHTML = "Try another option";
        
        document.querySelector('#outfit-viewer').innerHTML = '';
        
        if (responseJson.length === 0) {
            alert("No items in your closet that matches this search. Try adding more pieces to your closet!");
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
            
            
            let favoriteOutfitButton = document.querySelector('#favorite-outfit-button');
            if (!favoriteOutfitButton) {
                document.querySelector('#outfit-viewer').insertAdjacentHTML(
                    'beforebegin',
                    '<form id="favorite-outfit" action="/favorites" method="POST"><button class="buttons" value="Favorite" id="favorite-outfit-button"> FAVORITE </button></form>'
                    );
                    let favoriteOutfitButton = document.querySelector('#favorite-outfit-button');
                    
                    favoriteOutfitButton.addEventListener('click', (evt) => {
                        evt.preventDefault();
                        
                        const imgElements = document.getElementById("outfit-viewer");
                        
                        let listImgs = {};
                        
                        listImgs[0] = imgElements.firstChild.firstChild.getAttribute('data-id');
                        
                        
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
                    })
                };
            });
        };