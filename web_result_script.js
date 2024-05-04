//this code creates all the variables we use
var pageSize = 50;
var resultStartIndex = 0;
var resultEndIndex = Math.min(pageSize,results.length);
//this code sets up the text at the top
document.getElementById("query").innerText = "using query: " + query;
document.getElementById("total").innerText = "collected("+collectionUnique+" Unique). Filtered from "+scryfallTotalResults+" total results from Scryfall ";
//setup the drop down text options
updatePageSizes();
//setup the drop down on-clicks
setupDropDownClicks();
//create the initial images
setupImages(resultStartIndex,resultEndIndex);
//set the initial bounds text
updateBounds();

/****************************************/
/****************************************/
/****************************************/

function updateBounds(){
    document.getElementById("bounds").innerText = resultStartIndex.toString() + "-" + resultEndIndex.toString() +" of "+ results.length.toString();
}

function reload(){
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    location.reload();
}

//this is called by the pageSize buttons within the drop-down and they send themselves
function setPageSize(button){
    pageSize = Number(button.innerText);
    updatePageSizes();
    resultEndIndex = Math.min(resultStartIndex+pageSize,results.length);
    updateBounds();
    setupImages(resultStartIndex,resultEndIndex);
}

function updatePageSizes(){
    var pageSizeNumbers = [15,25,50,100];//dont change the number of pageSizeNumbers
    var pageSizes = document.getElementsByClassName("pagesize");
    var pscounter = 0;
    for (var i = 0; i < 4; i++){
        if (pageSizeNumbers[i] != pageSize){
            pageSizes[pscounter].innerText = pageSizeNumbers[i];     
            pscounter += 1;
        }
    }
    Array.from(document.getElementsByClassName("dropdownbutton")).forEach(inst=>inst.innerText = pageSize+" Per Page");
}

function dropDownFunction(){
    document.getElementById("subdropdown").classList.toggle("show");
}

function setupDropDownClicks(){
    window.onclick = function(event){
        if (!event.target.matches('.dropdownbutton')){
            var dropdowns = document.getElementsByClassName("dropdowncontent");
            for (var i = 0; i< dropdowns.length; i++){
                var openDropDown = dropdowns[i];
                if (openDropDown.classList.contains('show')){
                    openDropDown.classList.remove('show');
                }
            }
        }
    }
}

function setupImages(start,end){
    var resultImages = document.getElementById("results");
    resultImages.innerHTML = '';
    for (var i = start; i < end;i++){
        var image = document.createElement('img');
        image.src = results[i][0];
        image.style['cursor'] = "pointer";
        image.style['width']  = '20%';
        image.onClick = function(){window.open(results[i][1]),"_blank"};
        image.addEventListener("click",image.onClick);
        resultImages.appendChild(image);
    }
}

function prev(){
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    if (resultStartIndex != 0){
        resultStartIndex -= pageSize;
        resultEndIndex = resultStartIndex+pageSize
        updateBounds();
        setupImages(resultStartIndex,resultEndIndex);
    }
}

function next(){
    document.body.scrollTop = document.documentElement.scrollTop = 0;
    if ((resultStartIndex+pageSize) < results.length){
        resultStartIndex += pageSize;
        if ((results.length) > (resultEndIndex+pageSize)){
            resultEndIndex += pageSize;
        }else{
            resultEndIndex = results.length
        }
        updateBounds();
        setupImages(resultStartIndex,resultEndIndex);
    }
}
