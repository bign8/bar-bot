(function($) {

    // toggle drink lists
    $('a', '.list-categories').click(function(e) {
        e.preventDefault();
        var catid = $(e.currentTarget).data('catid');

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

    // add ingredient
    $('a', '.list-items').click(function(e) {
        e.preventDefault();
        // TODO
    });

})(jQuery);
