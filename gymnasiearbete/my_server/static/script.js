function setUnfavorite(id){
    html = `<button type="button" id="buttonFavorite-${id}" onclick="unFavorite('${id}')" class="btn btn-sm btn-outline-secondary">Unfavorite</button>`
    id = "buttonFavorite-"+id  
    $("#"+id).replaceWith(html);
}

function setFavorite(id){
    html = `<button type="button" id="buttonFavorite-${id}" onclick="favorite('${id}')" class="btn btn-sm btn-outline-secondary">Favorite</button>`
    id = "buttonFavorite-"+id  
    $("#"+id).replaceWith(html);
}

function favorite(id) {
    let path = $("#buttonFavorite-"+id).parent();
    link = path.children().last().children().last().attr('href')
    let path2 = path.parent()
    let name = path2.siblings("p").first().text()
    text = path2.siblings("p").eq(1).text().split(" ")
    price = text[0].split(":")[1]
    price_type = text[1]
    rating = path2.siblings("p").last().text()
    image = path2.siblings("img").first().attr('src')
    const product = {id:id ,name: name,price: price,price_type: price_type,rating: rating,description: null,image: image,link: link}
    $.ajax({
        type: "POST",
        url: "/product/favorite",
        contentType: "application/json",
        data: JSON.stringify({
            product: product
        }),
        dataType: "json",
        success: function () {
            setUnfavorite(id)
        }
    });
}

function unFavorite(id) {
    $.ajax({
        type: "POST",
        url: "/product/unfavorite",
        contentType: "application/json",
        data: JSON.stringify({
            id: id
        }),
        dataType: "json",
        success: function () {
            setFavorite(id)
        }
    });
}

$(document).ready(function() {

    $("#buttonProductSearch").click(function () {
        $.ajax({
            type: "POST",
            url: "/product/list/favorite",
            contentType: "application/json",
            data: "",
            dataType: "json",
            success: function (response) {
                favorites = response
    
                let keyword = $('#productSearch').val();
                if (keyword !== "") {
                    const settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "https://amazon24.p.rapidapi.com/api/product?categoryID=aps&keyword=" + keyword + "&country=US&page=1",
                        "method": "GET",
                        "headers": {
                            "X-RapidAPI-Host": "amazon24.p.rapidapi.com",
                            "X-RapidAPI-Key": "cca34353c8msh006522840d96800p18af71jsn7c68b7147423"
                        }
                    };
    
                    $.ajax(settings).done(function (response2) {
                        products = response2

                        html = ""

                        i = 0;
                        products["docs"].forEach(function (product) {
                            favorites.forEach(function (favorite) {
                                if (product.product_id == favorite) {
                                    html += '<div class="col"><div class="card shadow-sm"><div class="card-body">'
                                    html += '<img src="'+product.product_main_image_url+'" alt="Product image" style="width:150px;height:200px;">'
                                    html += '<p class="card-text">' + product.product_title + '</p>'
                                    html += '<p class="card-text">Price:' + product.app_sale_price + ' ' + product.app_sale_price_currency + '</p>'
                                    html += '<p class="card-text">Rating: ' + product.evaluate_rate + '</p>'
                                    html += '<div class="d-flex justify-content-between align-items-center"><div class="btn-group">'
                                    html += `<button type="button" id="buttonFavorite-${product.product_id}" onclick="unFavorite('${product.product_id}')" class="btn btn-sm btn-outline-secondary">Unfavorite</button>`
                                    html += '<button type="button" class="btn btn-sm btn-outline-secondary"><a href="' + product.product_detail_url + '">Link</a></button>'
                                    html += '</div><small class="text-muted"></small></div></div></div></div>'
                                    products["docs"].splice(i, 1)
                                    i -= 1;
                                }   
                            });
                            i += 1;
                        });
                                                
                        products["docs"].forEach(function (product) {
                            html += '<div class="col"><div class="card shadow-sm"><div class="card-body">'
                            html += '<img src="'+product.product_main_image_url+'" alt="Product image" style="width:150px;height:200px;">'
                            html += '<p class="card-text">' + product.product_title + '</p>'
                            html += '<p class="card-text">Price:' + product.app_sale_price + ' ' + product.app_sale_price_currency + '</p>'
                            html += '<p class="card-text">Rating: ' + product.evaluate_rate + '</p>'
                            html += '<div class="d-flex justify-content-between align-items-center"><div class="btn-group">'
                            html += `<button type="button" id="buttonFavorite-${product.product_id}" onclick="favorite('${product.product_id}')" class="btn btn-sm btn-outline-secondary">Favorite</button>`
                            html += '<button type="button" class="btn btn-sm btn-outline-secondary"><a href="' + product.product_detail_url + '">Link</a></button>'
                            html += '</div><small class="text-muted"></small></div></div></div></div>'
                        });
                        document.getElementById("productTable").innerHTML = html                      
                    });
                }
            }
        });
    });

    //Skapa en separat funktion för att sortera efter pris

});    