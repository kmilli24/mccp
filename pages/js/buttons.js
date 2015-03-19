/**
 * Created by drazisil on 3/16/15.
 */

function handleButton(cmd) {
    //noinspection JSUnresolvedFunction,JSUnusedLocalSymbols
    $.post("/cmd", {button: cmd, source: 'web'})
        .done(function (data) {
            location.reload();
        });
    return false;
}
