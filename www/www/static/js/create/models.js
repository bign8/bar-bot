/*
 * Ingredient Object
 */
var Ingredient = function (id, name) {
    this.id = id || -1;
    this.name = name || 'Unknown';
};
Ingredient.prototype = {
    equals: function(test) {
        return this.id == test.id;
    }
};
Ingredient.fromEle = function(ele) {
    return new Ingredient(
        $(ele).data('ing-id'),
        $('.media-heading', ele).text()
    );
};
Ingredient.fromJSON = function(json) {
    // TODO
};

/*
 * Amount Object
 */
var Amount = function (id, ingredient, amount) {
    this.id = id || -1;
    this.ingredient = ingredient || undefined;
    this.amount = amount || -1;
};
Amount.prototype = {
    set: function(value) {
        this.amount = value;
    },
    mod: function(delta) {
        this.amount += delta;
    }
};
Amount.fromJSON = function (json) {
    // TODO
};

/*
 * Recipe Object
 */
var Recipe = function(name) {
    this.id = -1; // recipe ID
    this.name = name || 'Name your drink'; // recipe name
    this.amounts = []; // values
    this.trash = {}; // ingredient.id -> deleted amount.id mapping
    this.listeners = [];
};
Recipe.prototype = {
    index: function(ingredient) {
        for (var i = 0; i < this.amounts.length; i++)
            if (this.amounts[i].ingredient.equals(ingredient))
                return i;
        return -1;
    },
    has: function(ingredient) {
        return this.index(ingredient) > -1;
    },
    find: function(ingredient) {
        var idx = this.index(ingredient);
        if (idx < 0) throw Error('Ingredient not found');
        return idx;
    },
    been_deleted: function(ingredient) {
        return this.trash.hasOwnProperty(ingredient.id);
    },
    generate_id: function(ingredient) {
        var test = this.been_deleted(ingredient);
        var value = test ? this.trash[ingredient.id] : -1;
        if (test) delete this.trash[ingredient.id];
        return value;
    },
    add: function(ingredient, value) {
        var idx = this.index(ingredient);
        if (idx > -1) throw Error('Ingredient already exists');

        var amount = new Amount(
            this.generate_id(ingredient),
            ingredient,
            value
        );
        this.amounts.push(amount);
        this.update();

        return amount;
    },
    get: function(ingredient) {
        var idx = this.find(ingredient);
        return this.amounts[idx];
    },
    set: function(ingredient, value) {
        if (value <= 0)
            return this.rem(ingredient);
        var idx = this.find(ingredient);
        this.amounts[idx].set(value);
        this.update();
    },
    rem: function(ingredient) {
        var idx = this.find(ingredient);
        this.trash[ingredient.id] = this.amounts[idx].id;
        delete this.amounts[idx];
        this.update();
    },
    mod: function(ingredient, delta) {
        var idx = this.find(ingredient);
        this.amounts[idx].mod(delta);
        if (this.amounts[idx].amount <= 0)
            return this.rem(ingredient);
        this.update();
    },
    toObj: function() {
        return {
            id: this.id,
            name: this.name,
            amounts: this.amounts,
            trash: this.trash
        };
    },
    toJSON: function() {
        return JSON.stringify(this.toObj());
    },
    register: function(cb) {
        this.listeners.push(cb);
    },
    update: function() {
        // TODO: frame delay this call
        for (var i = 0; i < this.listeners.length; i++)
            this.listeners[i]();
    }
};
Recipe.fromJSON = function(json) {
    // TODO
};

// VIEWS

var RecipeController = function (recipe) {
    this.recipe = recipe;
    recipe.register(this.update);
} ;
RecipeController.prototype = {
    update: function() {
        console.log('updated');
    }
};
