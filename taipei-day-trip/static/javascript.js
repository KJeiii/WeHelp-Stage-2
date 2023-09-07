const url = "/api/attractions?page=0"

// build function for creating html element
const createElement = (TagName, className) => {
    const element = document.createElement(TagName);
    element.setAttribute("class", className);
    return element;
};

const createBottomDivElement = (element) => {
    //在container裡面有12個element，1個element有：
    // 1. image > background > name
    // 2. intro > mrt & category

    // build element > image elemnt & intro element
    let bottomDivContainerElement = createElement("div", "bottomDiv-container-element");

    // build image elemet > background > name
    let bottomDivContainerImage = createElement("div", "bottomDiv-container-image");
    bottomDivContainerImage.style.backgroundImage = "url(" + element["images"][0] +")";
    let bottomDivContainerAttractionBackground = createElement("div", "bottomDiv-container-attractionBackground");
    let bottomDivContainerAttractionName = createElement("div", "bottomDiv-container-attractionName");
    bottomDivContainerAttractionName.textContent = element["name"];
    bottomDivContainerAttractionBackground.appendChild(bottomDivContainerAttractionName);
    bottomDivContainerImage.appendChild(bottomDivContainerAttractionBackground);

    // build intro > mrt & category
    let bottomDivContainerIntro = createElement("div", "bottomDiv-container-intro");
    let bottomDivContainerMrt = createElement("p", "bottomDiv-container-mrt");
    bottomDivContainerMrt.textContent = element["mrt"];
    let bottomDivContainerCategory = createElement("p", "bottomDiv-container-category");
    bottomDivContainerCategory.textContent = element["category"];
    bottomDivContainerIntro.appendChild(bottomDivContainerMrt);
    bottomDivContainerIntro.appendChild(bottomDivContainerCategory);

    // append child elements to bottomDivContainerElement, then to bottomDivContainer
    bottomDivContainerElement.appendChild(bottomDivContainerImage);
    bottomDivContainerElement.appendChild(bottomDivContainerIntro);
    return bottomDivContainerElement;
};

// recored nextPage
var nextPage = null;

const homePage = async() => {
    // get data from api
    let response = await fetch(url);
    let data = await response.json();
    let result = await data["data"];

    // update nextPage
    nextPage = data["nextPage"];

    // create elements dynamically
    let bottomDivContainer = createElement("div", "bottomDiv-container");

    result.forEach(element => { 
        let bottomDivContainerElement = createBottomDivElement(element);
        bottomDivContainer.appendChild(bottomDivContainerElement);
    });

    let bottomDiv = document.querySelector(".bottomDiv");
    bottomDiv.appendChild(bottomDivContainer);
};

homePage();
setTimeout(() => {console.log(nextPage)},1000);

// scroll page
options = {
    root: null,
    threshold: 1,
    rootMargin: "0px"
};

const observer = new IntersectionObserver ((entries, observer) => {
    entries.forEach((entry, observer) => {
        if (entry.isIntersecting) {
      
            // get api and create new elements
            fetch("/api/attractions?page=" + nextPage)
            .then(response => {
                if (!response.ok) {
                    console.log("Problem");
                    return;
                };
                return response.json();
            })
            .then(data => {
                // update nextPage
                nextPage = data["nextPage"];

                // create nextPage elements
                result = data["data"]
                let bottomDivContainer = document.querySelector(".bottomDiv-container");
                result.forEach(element => {
                    let bottomDivContainerElement = createBottomDivElement(element);
                    bottomDivContainer.appendChild(bottomDivContainerElement);
                });
            })
            .catch(error => {
                console.log(error);
            })

            console.log(entry.target.getBoundingClientRect().bottom);

            // // change tracking element
            // observer.unobserve(entry.target);
            // let lenthOfElement = document.querySelectorAll(".bottomDiv-container-element").length;
            // let elementForObserved = document.querySelectorAll(".bottomDiv-container-element")[lenthOfElement-1];
            // observer.observe(elementForObserved);
      
        };
    });
}, options);

setTimeout(() => {
    let lenthOfElement = document.querySelectorAll(".bottomDiv-container-element").length;
    let elementForObserved = document.querySelectorAll(".bottomDiv-container-element")[lenthOfElement-1];
    observer.observe(elementForObserved);
    console.log(elementForObserved.getBoundingClientRect().bottom);
}, 1000);


