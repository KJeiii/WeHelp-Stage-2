let //
attractionURL = window.location.href,
lenOfURL = attractionURL.length,
fetchURL = `/api/attraction/${attractionURL[lenOfURL-1]}`;
console.log(attractionURL);

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
    imgDiv = document.querySelector(".attraction-booking-img"),
    images = result["images"];

    imgDiv.style.backgroundImage = "url(" + images[0] +")";
    
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