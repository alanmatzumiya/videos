function print ( y ) {
    console.log(
        ( typeof(y) == "object" ) ? JSON.stringify( y ) : y
    );
};

function urlparse ( url, params ) {
    return url + "?" + Object.entries( params ).map(
        x => x[0] + "=" + x[1]
    ).join("&");        
};

function get ( url ) {
    var req = new XMLHttpRequest();
    req.open( "GET", url );
    req.send();
    req.onreadystatechange = function () {
        setTimeout( function () {
            print( req );
        }, 5e2 );
    };
};

function timeit ( secs ) {
    this.value = 0;
    this.interval = setInterval( function () {
        this.value++;
        if ( this.value > secs ) {
            clearInterval( this.interval );
            console.log( "time has finished" );
        } else {
            console.log( this.value );
        };
    }, 1e3 );
};

function newObj ( name ) {
    this.name = name;
    this.data = {};
};

newObj.prototype.setData = function ( data ) {
    var new_data = { ...this.data, ...data };
    this.data = new_data;
};

newObj.prototype.Timer = function ( secs ) {
    timeit( secs );
};
