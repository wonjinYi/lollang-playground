export default function enableTextareaTab(e, textarea) {
    e.preventDefault();
    textarea.setRangeText(
        '    ',
        textarea.selectionStart,
        textarea.selectionStart,
        'end'
    );
    
}