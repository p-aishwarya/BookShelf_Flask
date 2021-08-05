function handleClick(event){
    // alert("clicked hello")
    let val = document.forms["bookform"]["bookvalue"].value;
    console.log(val)
    if (val==""){
        alert("input is required")
    }
    // $.post( "/book",{
    //     bookform_data : x
    // });
    // $.get("/book", function(data) {
    //     console.log(data)
    // })
    var form = new FormData();
    form.append("bookform_data", val);

    var settings = {
    "url": "/book",
    "method": "POST",
    "timeout": 0,
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
    };

    $.ajax(settings).done(function (response) {
    // console.log(response);
    const dbParam = JSON.parse(response);
    let text = "<tbody>"
    for (let x in dbParam) {
        // console.log(dbParam[x])
        text+="<tr>"
        text += "<th scope='row'><a href='javascript: null' onclick='bookFunction(this.innerHTML)'>" + dbParam[x].isbn + "</a></th>";
        text+= "<td>"+dbParam[x].Title+"</td>"
        text+= "<td>"+dbParam[x].Author+"</td>"
        text+= "<td>"+dbParam[x].Year+"</td>"
        text+="</tr>"
    }  
    text+="</tbody>" 
    // console.log(text)
    document.getElementsByTagName("tbody")[0].innerHTML = text;
    });
}