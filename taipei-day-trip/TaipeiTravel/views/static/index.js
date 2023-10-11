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
    let bottomDivContainerElement = createElement("a", "bottomDiv-container-element");
    bottomDivContainerElement.style.display = "block";
    bottomDivContainerElement.setAttribute("href", `/attraction/${element["id"]}`);

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

// ------ recored nextPage and keword------
var nextPage = 0;
var keywordRecord;
var isloaded = false;

// ------ build function for create new attraction element ------
const loadPage = async(page, keyword) => {
    // console.log(page, keyword);

    // load next page unless nextPage = null
    if ( page !== null ) {

        // two way search depending on whether keyword is given
        var params_string;
        if (keyword === undefined) {
            params_string = "?page=" + page;
        }
        else {
            params_string = "?page=" + page + "&keyword=" + keyword;
        };
        
        // get data from api
        try {
            let response = await fetch("/api/attractions" + params_string);
            let data = await response.json();
            let result = await data["data"];
    
            // update nextPage
            nextPage = data["nextPage"];
            // console.log(`nextPage updated to ${nextPage}`);
            // console.log(`data amount to load ${result.length}`);
    
            // create elements dynamically
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
            result.forEach(element => { 
                let bottomDivContainerElement = createBottomDivElement(element);
                bottomDivContainer.appendChild(bottomDivContainerElement);
            })

            // update element to track
            let lenthOfElement = document.querySelectorAll('.bottomDiv-container-element').length;
            let elementForObserved = document.querySelectorAll('.bottomDiv-container-element')[lenthOfElement-1];
            observer.observe(elementForObserved);
            
            // turn off isloaded
            isloaded = false;
        }
        catch (error){
            console.log(error);
            console.log(response.status);

            // turn off isloaded in case of try condition is not triggered
            isloaded = false;
            return response.status;
        }
    }
    else{
        console.log("沒有下一頁");

        // turn off isloaded in case of if condition is not triggered
        isloaded = false;
    }
};

loadPage(nextPage, keywordRecord);


// ----- infinite scrolling -----
options = {
    root: null,
    threshold: 1,
    rootMargin: "0px"
};

const observer = new IntersectionObserver ((entries) => {
    if (entries[0].isIntersecting && !isloaded) {

        // remmove target for prevent fetching pulse
        observer.unobserve(entries[0].target);

        // change isLoaded state to update attraction
        isloaded = true;
        if (isloaded) {
            // update page
            if (nextPage !== null) {
                loadPage(nextPage, keywordRecord);
            };

            //keyword search and intersectingObserver could happen in same time
            //if intersectingObserver runs, but nextPage is null, it would not call loadPage function and it leads to 
            //not turning off the isLoaded inside loadPage function.
            //Herein, turn off isloaded here.
            isloaded = false; 
        }
    };
}, options);


// ------ update page by keyword searching ------
const searchKeyword = () => {

    let keyword = document.querySelector(".midDiv-container-searchBar-text").value;
    
    // initialize nextPage and update keword
    nextPage = 0;
    keywordRecord = keyword;
    console.log(`nextPage: ${nextPage}`);
    console.log(`kewordRecord: ${keywordRecord}`);


    fetch(`/api/attractions?page=${nextPage}&keyword=${keywordRecord}`)
    .then(response => {
        console.log(`isloaded state in before if ${isloaded}`);
        console.log(`response.ok before if ${response.ok}`);

        if (response.ok && !isloaded) { 
                        
            // remove all child element in bottomDiv-container
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
            while (bottomDivContainer.hasChildNodes()) {
            bottomDivContainer.removeChild(bottomDivContainer.firstChild);
            };

            // update attraction
            isloaded = true;
            if (isloaded) {
                loadPage(nextPage, keywordRecord);
            };
        }
        else{
            console.log(`isloaded state in else ${isloaded}`);

            // report no attraction text
            document.querySelector(".midDiv-container-searchBar-text").value = "無相符合景點";

            // remove all child element in bottomDiv-container
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
            while (bottomDivContainer.hasChildNodes()) {
            bottomDivContainer.removeChild(bottomDivContainer.firstChild);
            };
        }
    })
    .catch(error => {
        console.log(error);
        console.log(`isloaded state in catch ${isloaded}`);
    })

};


// ------ dynamically create mrt ------
const showMrt = async () => {
    // let url = "/api/mrts"

    try{
        let response = await fetch('/api/mrts');
        let data = await response.json();
        let result = await data["data"];

        let mrtDivMrtlistBarContent = document.querySelector(".mrtDiv-mrtlistBar-content");
        result.forEach(element => {
            let mrtDivMrtlistBarItem = createElement("div", "mrtDiv-mrtlistBar-item");
            mrtDivMrtlistBarItem.setAttribute("onclick", "searchMrt(this)")
            mrtDivMrtlistBarItem.textContent = element;
            mrtDivMrtlistBarContent.appendChild(mrtDivMrtlistBarItem);
        });
    }
    catch(error){
        console.log(error);
    }
};

showMrt();


// ----- scroll left or right when clicking arrow
const moveLeft = () => {
    let mrtDivMrtlistBarContent = document.querySelector(".mrtDiv-mrtlistBar-content");
    mrtDivMrtlistBarContent.scrollLeft += 80;
};

const moveRight = () => {
    let mrtDivMrtlistBarContent = document.querySelector(".mrtDiv-mrtlistBar-content");
    mrtDivMrtlistBarContent.scrollLeft -= 80;
};

// ------ update page by mrt searching ------
const searchMrt = element => {
    let keyword = element.textContent;

    // updatae text in attraction searching input
    document.querySelector(".midDiv-container-searchBar-text").value = keyword;

    // remove all child element in bottomDiv-container
    let bottomDivContainer = document.querySelector(".bottomDiv-container");
    while (bottomDivContainer.hasChildNodes()) {
    bottomDivContainer.removeChild(bottomDivContainer.firstChild);
    };

    // initialize nextPage and update keyword
    nextPage = 0;
    keywordRecord = keyword;

    // update attraction
    loadPage(nextPage, keywordRecord);
};

