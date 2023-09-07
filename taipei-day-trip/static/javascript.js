const url = "/api/attractions"

// ----- build function for creating html element -----
const createElement = (TagName, className) => {
    const element = document.createElement(TagName);
    element.setAttribute("class", className);
    return element;
};

// ----- dynamically create homepage attraction element -----
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
var nextPage = 0;

// build function for create new attraction element
const loadPage = async(page, keyword) => {
    if ( page !== null ) {
        let params_string;
        if (keyword === undefined) {
            params_string = "?page=" + page;
        }
        else {
            params_string = "?page=" + page + "&keyword=" + keyword;
        }
        
        // get data from api
        try {
            let response = await fetch(url + params_string);
            let data = await response.json();
            let result = await data["data"];

            if (!response.ok) {
                console.log(response.status, typeof(response.status));
                return response.status;
            }
    
            // update nextPage
            nextPage = data["nextPage"];
    
            // create elements dynamically
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
    
            result.forEach(element => { 
                let bottomDivContainerElement = createBottomDivElement(element);
                bottomDivContainer.appendChild(bottomDivContainerElement);
            
            return response.status;
            })
        }
        catch (error){
            console.log(error);
            console.log(response.status);
            return response.status;
        }
    }
};

loadPage(nextPage);


// ----- infinite scrolling -----
options = {
    root: null,
    threshold: 1,
    rootMargin: "0px"
};

const observer = new IntersectionObserver ((entries, observer) => {
    entries.forEach((entry, observer) => {
        if (entry.isIntersecting) {
            setTimeout(loadPage(nextPage),500);

            // change tracking element
                // removeObserveEntity(entry);
                // createBottomDivElement();
            };
        });
    }, options);

let footerDiv = document.querySelector(".footerDiv");
observer.observe(footerDiv);
    
      



// ----- build function for adding new entry for IntersectionObserver -----


// const createObserveEntiy = () => {
//     let lenthOfElement = document.querySelectorAll('.bottomDiv-container-element').length;
//     let elementForObserved = document.querySelectorAll('.bottomDiv-container-element')[lenthOfElement-1];
//     observer.observe(elementForObserved);
// };

// const removeObserveEntity = (entry) => {
//     observer.unobserve(entry.target);
// };



// search attraciton
const searchKeyword = () => {

    let keyword = document.querySelector(".midDiv-container-searchBar-text").value;
    if (loadPage(nextPage, keyword) === 200) {

        // remove all child element in bottomDiv-container
        let bottomDivContainer = document.querySelector(".bottomDiv-container");
        while (bottomDivContainer.hasChildNodes()) {
        bottomDivContainer.removeChild(bottomDivContainer.firstChild);
        };

        // instalize nextPage
        nextPage = 0;

        // update attraction
        loadPage(nextPage, keyword);
    }
    else{
        document.querySelector(".midDiv-container-searchBar-text").value = "無相符合景點";
    }
};

const showMrt = async () => {
    let url = "/api/mrts"

    try{
        let response = await fetch(url);
        let data = await response.json();
        let result = await data["data"];
        console.log(result);

        // dynamically create mrt 
        let mrtDivMrtlistBarContent = document.querySelector(".mrtDiv-mrtlistBar-content");
        result.forEach(element => {
            let mrtDivMrtlistBarItem = createElement("div", "mrtDiv-mrtlistBar-item");
            mrtDivMrtlistBarItem.textContent = element;
            mrtDivMrtlistBarContent.appendChild(mrtDivMrtlistBarItem);
        });
    }
    catch(error){
        console.log(error);
    }
};

showMrt();
