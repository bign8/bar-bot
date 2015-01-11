(function($) {

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
        // TODO
    });

})(jQuery);
