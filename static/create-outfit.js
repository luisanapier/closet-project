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
        // clear out the previous options if any
        
        Object.values(responseJson).forEach((item) => {
            document.querySelector('#outfit-viewer').insertAdjacentHTML(
                'beforeend', 
                `<div><img 
                width=200px; 
                display: inline-block; 
                src="${item}"/></div>`
            );
        });
            
        document.querySelector('input#generate-other-outfit-button').style.display = "block";
        document.querySelector('input#favorite-outfit-button').style.display = "block";
    // // If you want to remove the form when results are shown
    // document.querySelector('#create-outfit-form').style.display = 'none';
});
};

const generateAnotherOutfitButton = document.querySelector('input#generate-other-outfit-button');
console.log(generateAnotherOutfitButton);
generateAnotherOutfitButton.addEventListener('click', handleClick);