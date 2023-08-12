

function setParentChecked(input) {
    const parentId = input.getAttribute('parentId');
    if (!parentId) return;
    const parent = document.getElementById(parentId);
    if (!parent) return;
    const siblings = $('input[parentId="'+parentId+'"]').toArray();
    let hasAnyElseChecked = siblings
        .map(function (k) { return k.checked; })
        .reduce(function (a, b) { return a || b; }, false);
    parent.checked = hasAnyElseChecked
    setParentChecked(parent);
}