let //
attractionURL = window.location.href,
listOfURL = attractionURL.split("/"),
lenOfList = listOfURL.length,
fetchURL = `/api/attraction/${listOfURL[lenOfList-1]}`;

let amountOfImages;

// ----- auto fill content using /api/attraction/<attraction_id> -----

const fillContent = (cssSelector, content) => {
    let element = document.querySelector(cssSelector);
    element.textContent = content;
};


const loadPage = async () => {
    try {
    
    // get data from api
    let //
    response = await fetch(fetchURL),
    data = await response.json(),
    result = await data["data"];

    // create elements
    // attraction-booking-img
    let //
    imgGalleryElements = document.querySelector(".attraction-imgGallery-elements"),
    images = result["images"];
    console.log(images.length);

    images.forEach(image => {
        let imageItem = document.createElement("img");
        imageItem.setAttribute("src", image);
        // imageItem.style.zIndex = 1;
        imgGalleryElements.appendChild(imageItem);

        console.log('Done')
    });
    
    // attraction-booking-name
    fillContent(".attraction-booking-name", result["name"]);
    
    // attraction-booking-CatMRT
    let content = `${result["category"]}at${result["mrt"]}`;
    fillContent(".attraction-booking-CatMRT", content);

    // detail-intro
    fillContent(".detail-intro", result["description"]);

    // address-content
    fillContent(".address-content", result["address"]);

    // transport-content
    fillContent(".transport-content", result["transport"]);

    }
    catch(error) {
        console.log(error)
    }   

};

loadPage();


// ----- interval fee exchange-----
const feeExchange = () => {

    let //
    beforenoonChecked = document.querySelector(".interval-beforenoon").checked,
    afternoonChecked = document.querySelector(".interval-afternoon").checked,
    feeSpan = document.querySelector(".interval-fee");

    if (beforenoonChecked) {
        feeSpan.textContent = "新台幣 2000 元";
    };

    if (afternoonChecked) {
        feeSpan.textContent = "新台幣 2500 元";
    };
}


// ----- scroll left or right when clicking arrow -----
const moveLeft = () => {
    let //
    elements = document.querySelector(".attraction-imgGallery-elements"),
    movingLength = elements.clientWidth;
    
    elements.scrollLeft -= movingLength;
};

const moveRight = () => {
    let //
    elements = document.querySelector(".attraction-imgGallery-elements"),
    movingLength = elements.clientWidth;

    elements.scrollLeft += movingLength;

};