let //
attractionURL = window.location.href,
listOfURL = attractionURL.split("/"),
lenOfList = listOfURL.length,
fetchURL = `/api/attraction/${listOfURL[lenOfList-1]}`;

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
    // let //
    // imgDiv = document.querySelector(".attraction-booking-imgGallery"),
    // images = result["images"];

    // imgDiv.style.backgroundImage = "url(" + images[0] +")";
    
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
