var decodeEntities = (function() {
    // this prevents any overhead from creating the object each time
    var element = document.createElement("div");
    element.className += " mermaid-graph";

    function decodeHTMLEntities(str) {
        if (str && typeof str === "string") {
            // strip script/html tags
            str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gim, "");
            str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gim, "");
            element.innerHTML = str;
            str = element.textContent;
            element.textContent = "";
        }

        return str;
    }

    return decodeHTMLEntities;
})();

$(function() {
    var insertSvg = function(svgCode, bindFunctions) {
        var graph = document.createElement("div");
        graph.className += ' ' + new Date().getTime();
        graph.setAttribute("id", "graph-div");
        document.body.appendChild(graph);
        graph.innerHTML = svgCode;
        console.log(svgCode);
    };

    let graphDiv = document.querySelector("#graph-definition");
    let render = document.querySelector("#render");
    let status = document.querySelector('[labelFor="#graph-definition"]');

    function renderGraph() {
        console.log('about to decode');
        var graphDefinition = decodeEntities(document.querySelector("#graph-definition").value);
        
        try {
            document.querySelector("#graph-div").remove();
            console.log("deleting old svg wrapper element");
        } catch (e) {
            console.log("no existing graph found");
        }

        // mermaid.init();
        console.log(graphDefinition);

        if (mermaid.parse(graphDefinition)) {
            status.classList.remove('error');
            status.classList.add('ok');
        }
        else {
            status.classList.add('error');
            status.classList.remove('ok');
        }

        var graph = mermaidAPI.render("graph-diagram", graphDefinition, insertSvg);
    }
  
    var delayRenderingTimeout;
    var delayTime = 0.5;
    var delayRendering = function() {
        clearTimeout(delayRenderingTimeout);
        delayRenderingTimeout = setTimeout(renderGraph, delayTime * 1000);
    }

    renderGraph();
    graphDiv.addEventListener("change", renderGraph);
    graphDiv.addEventListener("keyup", delayRendering);
    render.addEventListener("click", renderGraph);
});
