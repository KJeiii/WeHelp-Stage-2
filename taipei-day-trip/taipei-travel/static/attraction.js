let //
attractionURL = window.location.href,
listOfURL = attractionURL.split("/"),
lenOfList = listOfURL.length,
fetchURL = `/api/attraction/${listOfURL[lenOfList-1]}`;

// create global varibles to record images amount and dot status
var//
imagesAmount,
dotmonitered = 0;
console.log(`dotmonitered: ${dotmonitered}`);


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

    // image dots
    // recored imagesAmount to global variable
    imagesAmount = images.length;
    console.log(`imagesAmount: ${imagesAmount}`);

    images.forEach(image => {
        let imageItem = document.createElement("div");
        imageItem.setAttribute("class", "attraction-imgGallery-item");
        imageItem.style.backgroundImage = `url(${image})`;
        imgGalleryElements.appendChild(imageItem);

        let//
        dotsContainer = document.querySelector(".attraction-imgGallery-dotsContainer"),
        dots = document.createElement("img");
        dots.setAttribute("src", "../static/image/attraction-dot-white.svg");

        dotsContainer.appendChild(dots);
    });

    // replace first white dot with black dot
    let firstDot = document.querySelectorAll(".attraction-imgGallery-dotsContainer img")[0];
    firstDot.setAttribute("src", "../static/image/attraction-dot-black.svg");
    
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

    // scroll images
    let //
    elements = document.querySelector(".attraction-imgGallery-elements"),
    movingLength = elements.clientWidth;
    
    elements.scrollLeft -= movingLength;

    // scroll dots
    let//
    dots = document.querySelectorAll(".attraction-imgGallery-dotsContainer img");

    // change dotmonitered to white and "dotmonitered - 1" to black
    if (dotmonitered - 1 >= 0) {
        dots[dotmonitered].setAttribute("src", "../static/image/attraction-dot-white.svg");
        dots[dotmonitered - 1].setAttribute("src", "../static/image/attraction-dot-black.svg");
        dotmonitered -= 1;
    }
};

const moveRight = () => {

    // scroll images
    let //
    elements = document.querySelector(".attraction-imgGallery-elements"),
    movingLength = elements.clientWidth;

    elements.scrollLeft += movingLength;

    // scroll dots
    let//
    dots = document.querySelectorAll(".attraction-imgGallery-dotsContainer img");

    // change dotmonitered to white and "dotmonitered + 1" to black
    if (dotmonitered + 1 < imagesAmount) {
        dots[dotmonitered].setAttribute("src", "../static/image/attraction-dot-white.svg");
        dots[dotmonitered + 1].setAttribute("src", "../static/image/attraction-dot-black.svg");
        dotmonitered += 1;
    }
};

// booking itinerary
function bookItinerary() {
    SignStatus().then((result) => {
        console.log(result);
        if (result["ok"] === true) {
            let// 
            time = "beforenoon",
            interval = document.querySelectorAll("input[type=radio]");

            if (interval[1].checked === true) {
                time = "afternoon";
            }
        
            let itineraryInfo = {
                "attraction_id": listOfURL[lenOfList-1],
                "date": document.querySelector("input[type=date]").value,
                "time": time,
                "price": document.querySelector(".interval-fee").textContent.split(" ")[1]
            };

            fetch("/api/booking",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "authorization": `Bearer ${window.localStorage.getItem("token")}`
                },
                body: JSON.stringify(itineraryInfo)
            })
            .then((response) => {
                console.log(response.json());
                window.location.replace("/booking");
            })
            .catch((error) => {
                console.log(error);
            });
        }
        else {
            Member();
            SignInSwitch();
        }
    });
};