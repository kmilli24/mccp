/**
 * Created by drazisil on 3/16/15.
 */

function handleButton(cmd) {
    $.post("/cmd", {button: cmd, source: 'web'})
        .done(function (data) {
            location.reload();
        });
    return false;
}
