import 'js-loading-overlay';

function startLoading(){
    JsLoadingOverlay.show({
        'overlayBackgroundColor': '#666666',
        'overlayOpacity': 0.6,
        'spinnerIcon': 'pacman',
        'spinnerColor': '#FFF',
        'spinnerSize': '3x',
        'overlayIDName': 'overlay',
        'spinnerIDName': 'spinner',
        'spinnerZIndex':99999,
        'overlayZIndex':99998
    });
}

function finishLoading(){
    JsLoadingOverlay.hide();
}

export {startLoading, finishLoading};