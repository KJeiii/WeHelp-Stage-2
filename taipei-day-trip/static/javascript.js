// const url = "http://3.106.20.120/api/attractions"

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

// ------ recored nextPage and keword------
var nextPage = 0;
var keywordRecord;
var isloaded = true;

// ------ build function for create new attraction element ------
const loadPage = async(page, keyword) => {
    console.log(page, keyword);

    // load next page unless nextPage = null
    if ( page !== null ) {
        // two way search depending on whether keyword is given
        var params_string;
        if (keyword === undefined) {
            params_string = "?page=" + page;
        }
        else {
            params_string = "?page=" + page + "&keyword=" + keyword;
        }
        
        // get data from api
        try {
            let response = await fetch("http://3.106.20.120:3000/api/attractions" + params_string);
            let data = await response.json();
            let result = await data["data"];
    
            // update nextPage
            nextPage = data["nextPage"];
            console.log(`nextPage updated to ${nextPage}`);
            console.log(`data amount to load ${result.length}`);
    
            // create elements dynamically
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
    
            result.forEach(element => { 
                let bottomDivContainerElement = createBottomDivElement(element);
                bottomDivContainer.appendChild(bottomDivContainerElement);
            
            })
        }
        catch (error){
            console.log(error);
            console.log(response.status);
            return response.status;
        }
    }
    else{
        console.log("沒有下一頁")
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
    if (entries[0].isIntersecting) {
        // remmove target for prevent fetching pulse
        observer.unobserve(entries[0].target);

        if (isloaded) {
            // update page
            if (nextPage !== null) {
                isloaded = false;
                loadPage(nextPage, keywordRecord);
    
                setTimeout(() => {
                    let lenthOfElement = document.querySelectorAll('.bottomDiv-container-element').length;
                    let elementForObserved = document.querySelectorAll('.bottomDiv-container-element')[lenthOfElement-1];
                    observer.observe(elementForObserved);
                }, 500)
                isloaded = true;
            }

        }
    };
}, options);


setTimeout (() => {
    let lenthOfElement = document.querySelectorAll('.bottomDiv-container-element').length;
    let elementForObserved = document.querySelectorAll('.bottomDiv-container-element')[lenthOfElement-1];
    observer.observe(elementForObserved);

},1000);



// ------ update page by keyword searching ------
const searchKeyword = () => {

    let keyword = document.querySelector(".midDiv-container-searchBar-text").value;
    
    // initialize nextPage and update keword
    nextPage = 0;
    keywordRecord = keyword;
    console.log(`nextPage: ${nextPage}`);
    console.log(`kewordRecord: ${keywordRecord}`);


    fetch(`/api/attractions?page=${nextPage}&keyword=${keyword}`)
    .then(response => {
        if (!response.ok) { 

            // report no attraction text
            document.querySelector(".midDiv-container-searchBar-text").value = "無相符合景點";

            // remove all child element in bottomDiv-container
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
            while (bottomDivContainer.hasChildNodes()) {
            bottomDivContainer.removeChild(bottomDivContainer.firstChild);
            };
        }
        else{
            // remove all child element in bottomDiv-container
            let bottomDivContainer = document.querySelector(".bottomDiv-container");
            while (bottomDivContainer.hasChildNodes()) {
            bottomDivContainer.removeChild(bottomDivContainer.firstChild);
            };

            // update attraction
            loadPage(nextPage, keywordRecord);

            // update element for intersection observation
            setTimeout (() => {
                let lenthOfElement = document.querySelectorAll('.bottomDiv-container-element').length;
                let elementForObserved = document.querySelectorAll('.bottomDiv-container-element')[lenthOfElement-1];
                observer.observe(elementForObserved);
            },500);
        }
    })
    .catch(error => {
        console.log(error);
    })

};


// ------ dynamically create mrt ------
const showMrt = async () => {
    // let url = "/api/mrts"

    try{
        let response = await fetch('http://3.106.20.120:3000/api/mrts');
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

    // update element for intersection observation
    setTimeout (() => {
        let lenthOfElement = document.querySelectorAll('.bottomDiv-container-element').length;
        let elementForObserved = document.querySelectorAll('.bottomDiv-container-element')[lenthOfElement-1];
        observer.observe(elementForObserved);
    },500);

};