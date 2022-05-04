$(document).ready(function() {

  function ajaxCallRequest(f_method, f_url, f_data) {
    var f_contentType = 'application/json';
    $.ajax({
      url: f_url,
      type: f_method,
      contentType: f_contentType,
      dataType: 'json',
      data: f_data,
      success: function(data) {
        var jsonResult = JSON.stringify(data);
        console.log(jsonResult)

      }
    });
  }

  $(document).on('click', '.btn-add', function(event) {
    event.preventDefault();
    var controlForm = $('.controls');
    var currentEntry = $(this).parents('.entry:first');
    var newEntry = $(currentEntry.clone()).appendTo(controlForm);
    newEntry.find('input').val('');
    controlForm.find('.entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<span class="glyphicon glyphicon-minus"></span>');

    var inputs = $('.controls .form-control');
    $.each(inputs, function(index, item) {
      item.name = 'emails[' + index + ']';
    });
  });

  $(document).on('click', '.btn-remove', function(event) {
    event.preventDefault();
    $(this).parents('.entry:first').remove();
    var inputs = $('.controls .form-control');
    $.each(inputs, function(index, item) {
      item.name = 'emails[' + index + ']';
    });
  });

  $(document).on('click', '.btn-remove', function(event) {
    e.preventDefault();
    alert('remove');
  });


  $("#btn_createNewPrice").click(function(event) {
    event.preventDefault();
    var form = $('#newPrice');
    var method = form.attr('method');
    var url = form.attr('action');
    var arrayData = $(form).serializeArray();
    var jsonObj = {};
    for (var i = 0, j = arrayData.length; i < j; i++)
    {
        var element = document.getElementById(arrayData[i].name);
            if(element.name.startsWith('btn_'))
    {
        jsonObj[arrayData[i].name]=element.value;}

    }
    var data = JSON.stringify(jsonObj);
    console.log(data);
    ajaxCallRequest(method, url, data);
  });
  $.mockjax({
    url: '/ajaxRequest/serialized/',
    type: 'POST',
    contentType: 'text/json',
    responseTime: 0,
    response: function(settings) {
      var data = settings.data;
      this.responseText = data;
    }
  });

  });

  $("#sendTreeJSon").click(function(event) {
    event.preventDefault();
    var form = $('#ajaxForm');
    var method = form.attr('method');
    var url = form.attr('action') + 'treejson/';
    var jsonData = $(form).serializeObject();
    console.log(jsonData);
    ajaxCallRequest(method, url, jsonData);
  });

  $.mockjax({
    url: '/ajaxRequest/treejson/',
    type: 'POST',
    contentType: 'text/json',
    responseTime: 0,
    response: function(settings) {
      var data = settings.data;
      this.responseText = data;
    }
  });

  $("#defaultData").click(function(event) {
    event.preventDefault();
    $('#firstname').val('Mortadelo');
    $('#lastname').val('Filemon');
    $('#address_street').val('Rua del Percebe 13');
    $('#address_city').val('Madrid');
    $('#address_zip').val('28010');
    $("[name='emails[0]']").val('superintendencia@cia.es');
  });
