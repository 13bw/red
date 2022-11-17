$(document).ready(function() {
    var results = $("#results")
    var socket = io.connect();

    $('form#search').submit(function(event) {
        socket.emit('search', { data: $('#search_data').val() });
        results.empty()
        return false;
    });

    socket.on("getQuery", (query) => {
        $.each(query, function(loja, lojaData) {
            results.append(`<div id="${loja}" class="slides">`)

            lojaElem = $(`#${loja}`)
            lojaElem.append(`<h3> ${loja} </h3>`)

            $(lojaData).each(function(idx, data) {
                lojaElem.append(`<div class="produto"> <img src="${data.imagem}" alt=""><div class="nomeproduto">${data.nome}</div><div class="precoproduto">${data.preco}</div></div>`)
            })
        })


    })


});