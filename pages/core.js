/**
 * Created by drazisil on 3/16/15.
 */
var lastUpdateTimeStamp = '';

function handleInput(cmd) {
    $.post("/cmd", {cmd: cmd, source: 'web'});
    $("#cmd").val("");
    return false;
}

function updateStatus(status) {
    var statusIcon = $("#statusIcon");
    switch (status) {
        case "stopped":
            statusIcon.attr('src', 'img/red.png');
            break;
        case 'running':
            statusIcon.attr('src', 'img/green.png');
            break;
        case 'starting':
        case 'stopping':
        case 'restarting':
            statusIcon.attr('src', 'img/yellow.png');
            break
    }
    statusIcon.attr('alt', status);
    statusIcon.attr('title', status);

}

var myAjaxCall = function () {
    //noinspection JSUnusedGlobalSymbols
    $.ajax({
        type: "GET",
        url: '/term',
        dataType: "json",
        success: function (json) {
            if (json.timestamp > lastUpdateTimeStamp) {
                updateStatus(json.status);
                var term = $('#term-display');
                var tmpReply = [];
                //noinspection JSUnresolvedVariable
                tmpReply = json.output.join("<br>");
                term.html(tmpReply.toString());
                lastUpdateTimeStamp = json.timestamp;
                //noinspection JSValidateTypes
                term.scrollTop(term[0].scrollHeight);
            }
        }
    })
};

window.onload = function () {
    window.setInterval('myAjaxCall()', 1000); // 60 seconds

};
