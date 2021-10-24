var pb = new PolyBuffer(jsarguments[1]);
var dFileIndex = new Dict(jsarguments[1]);
var sampleList = new Array();
var sampleRate = new Array();
var posList = new Array();
var srcCount = 1;

function openwindow() {
    pb.open();
}


function closewindow() {
    pb.wclose();
}

function append(fileName) {
    pb.append(fileName);
    dFileIndex.set(fileName, srcCount);
    sampleRate.push(parseFloat(pb.dump()[pb.dump().length - 1]) / 1000);
    srcCount = srcCount + 1;
}

function fileIndex(fileName) {
    outlet(0, dFileIndex.get(fileName));
}

function clear() {
    pb.clear();
    dFileIndex.clear();
    sampleList = [];
    posList = [];
    sampleRate = [];
    srcCount = 1;
}


function oscGrain() {
    var curSamples = arrayfromargs("newGrain", arguments);
    sampleList = [];
    posList = [];

    for(i = 0; i < parseInt(curSamples[1]); i++) {
        sampleList.push(curSamples[i * 3 + 2]);
        posList.push(curSamples[i * 3 + 3]);
    }
}

function newGrain() {
    var curSamples = arrayfromargs("newGrain", arguments);
    sampleList = [];
    posList = [];
    for(i = 1; i < curSamples.length; i+=2) {
        sampleList.push(curSamples[i]);
        posList.push(curSamples[i+1]);

    }
}


function getGrain(){
    if(sampleList.length > 0) {
        var i = Math.floor(Math.random() * sampleList.length);
        var srcIndex = parseInt(dFileIndex.get(sampleList[i]));
        outlet(0, [jsarguments[1] + "." + srcIndex, posList[i] / sampleRate[srcIndex - 1]]);
    }
}