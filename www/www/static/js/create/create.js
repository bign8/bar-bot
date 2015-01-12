var for_testing = new Recipe();
(function($, recipe) {

    // toggle drink lists
    $('a', '.list-categories').click(function(e) {
        e.preventDefault();
        var ele = $(e.currentTarget);
        var catid = ele.data('catid');
        document.location = '#' + ele.data('cat');

        // hide/show all lists
        $('.list-items').each(function(i, ele) {
            ele = $(ele);
            is_active = ele.data('catid') == catid;
            ele[is_active ? 'removeClass' : 'addClass']('hide');
        });

        // toggle active status
        $('a', '.list-categories').each(function(i, ele) {
            ele = $(ele);
            is_active = ele.data('catid') == catid;
            ele[is_active ? 'addClass' : 'removeClass']('active');
        });
    });

    var active_cat = document.location.hash.replace('#', '');
    if (active_cat) $('a[data-cat="' + active_cat + '"]', '.list-categories').click();

    // add ingredient
    $('a', '.list-items').click(function(e) {
        e.preventDefault();

        // don't add it conditions
        var ele = $(e.currentTarget);
        if (ele.hasClass('disabled'))
            throw Error('Ingredient is disabled');
        if (ele.hasClass('active'))
            return ele.removeClass('active');

        // Cleanup lists
        $('a', '.list-items').removeClass('active');
        ele.addClass('active');

        // Add or get amount from recipe
        var ing = Ingredient.fromEle(e.currentTarget);
        var active = recipe.has(ing) ? recipe.get(ing) : recipe.add(ing);

        // TODO: do graphics stuff with active element
        console.log(active);
    });
})(jQuery, for_testing);
