  var $table = $('#table')
  var $remove = $('#remove')
  var selections = []

  function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
      return row.id
    })
  }

  function responseHandler(res) {
    $.each(res.rows, function (i, row) {
      row.state = $.inArray(row.id, selections) !== -1
    })
    return res
  }

  function detailFormatter(index, row) {
    var html = []
    $.each(row, function (key, value)
    {
        if (typeof value == "object")
        {
            html.push('<p><b>' + key + ':</b> ')
            $.each(value,function(innerKey,innerValue)
            {
                html.push('<p style="text-indent: 1em;">' + innerKey + ': ' + innerValue + '</p>')
            })
        }
        else{
            html.push('<p><b>' + key + ':</b> ' + value + '</p>')
        }
    })
    return html.join('')
  }

  function checkboxFormatter(data){
  var state = false
  state = data
  if(state){return 'on'}else{return'off'}

  }

  function initTable() {
    $table.bootstrapTable('destroy').bootstrapTable({
      height: 550,
      locale: $('#locale').val(),
      columns: [
        {
          field: 'state',
          checkbox: true,
          rowspan: 1,
          align: 'center',
          valign: 'middle'
        }, {
          title: 'Item ID',
          field: 'id',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true
        },
        {
          field: 'type',
          title: 'Type',
          sortable: true,
          align: 'center'
        }, {
          field: 'description',
          title: 'Description',
          sortable: true,
          align: 'center'
        },{
          field: 'deposit',
          title: 'Deposit?',
          checkbox: true,
          sortable: true,
          align: 'center',
          detailFormatter: checkboxFormatter
        }
        ]
    })
    $table.on('check.bs.table uncheck.bs.table ' +
      'check-all.bs.table uncheck-all.bs.table',
    function () {
      $remove.prop('disabled', !$table.bootstrapTable('getSelections').length)

      // save your data, here just save the current page
      selections = getIdSelections()
      // push or splice the selections if you want to save all data selections
    })
    $table.on('all.bs.table', function (e, name, args) {
      console.log(name, args)
    })
    $remove.click(function () {
      var ids = getIdSelections()
      ids.forEach( function(id)
      {deleteRow(id);      })
      $table.bootstrapTable('remove', {
        field: 'id',
        values: ids
      })
      $remove.prop('disabled', true)
    })
  }

function deleteRow(id){
    var method = 'DELETE';
    var url = '/api/v0/transactiontype/'+id;
    ajaxCallRequest(method, url);
    }


$(function() {
    initTable()
    $('#locale').change(initTable)
  })


$("#btn_createNewTransactionType").click(function(event) {
    event.preventDefault();
    var form = $('#newTransactionType');
    if (form[0].checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
           form[0].classList.add('was-validated');
           return;
        }
    var method = 'POST';
    var url = '/api/v0/transactiontype';
    var arrayData = $(form).serializeArray();
    var jsonObj = {};
    for (var i = 0, j = arrayData.length; i < j; i++)
    {
        var element = document.getElementById(arrayData[i].name);
            if(!element.name.startsWith('btn_'))
            {
            if (element.type=='checkbox'){
            jsonObj[arrayData[i].name]=element.checked;
            }else{
                jsonObj[arrayData[i].name]=element.value;}
            }
    }
    var data = JSON.stringify(jsonObj);
    console.log(data);
    ajaxCallRequest(method, url, data);
  });

 function ajaxCallRequest(f_method, f_url, f_data=null) {
    var f_contentType = 'application/json';
    $.ajax({
      url: f_url,
      type: f_method,
      contentType: f_contentType,
      dataType: 'json',
      data: f_data,
      success: function(data) {
        var jsonResult = JSON.stringify(data);
        //$("#results").val(unescape(jsonResult));
        console.log(jsonResult)

      }
    });
  }
