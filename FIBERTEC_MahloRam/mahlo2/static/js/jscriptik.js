
$(function () {

    function killSetTimout() {
        $.ajax({
            url: "/logoff",
            type: "post",
            success: function (data) {
                clearInterval(xTimeout);
                setWinLoc("/signup");

            },
        });
    }

    function addMinutes(date, minutes) {
        return new Date(date.getTime() + minutes * 60000);
    }
    function setWinLoc(loc) {
        window.location = loc;
    }
    function dajObrazok(parIdentita, parUtl, parLtl, parTyp) {
        let casZaciatok = $("#NahledModalNastavenieZacatek").val();
        let casKoniec = $("#NahledModalNastavenieKonec").val();
        parseAjax("/get_img", { 'identity': parIdentita, "casZaciatok": casZaciatok, "casKoniec": casKoniec, 'ltl': parLtl, 'utl': parUtl, 'typ': parTyp }, function (urlka) {

            let nodeHeat = document.getElementById('NahledImgHeat');
            let nodeHist = document.getElementById('NahledImgHist');

            $('#NahledImgHeat').attr('src', urlka.urlmoje);
            $('#NahledImgHist').attr('src', urlka.urlHist);

            let nod = $('.legend-labels li span');

            Object.values(nod)[0].innerHTML = (urlka.lst[0]);
            Object.values(nod)[3].innerHTML = (urlka.lst[1]);
            Object.values(nod)[4].innerHTML = (urlka.lst[2]);
            Object.values(nod)[5].innerHTML = (urlka.lst[3]);
            Object.values(nod)[6].innerHTML = (urlka.lst[4]);
            Object.values(nod)[7].innerHTML = (urlka.lst[5]);
            Object.values(nod)[8].innerHTML = (urlka.lst[6]);
            Object.values(nod)[9].innerHTML = (urlka.lst[7]);
            Object.values(nod)[9].style.color = "white";
            Object.values(nod)[10].innerHTML = (urlka.lst[8]);
            Object.values(nod)[10].style.color = "white";
            Object.values(nod)[11].innerHTML = (urlka.lst[9]);
            Object.values(nod)[11].style.color = "white";
            Object.values(nod)[12].innerHTML = (urlka.lst[10]);
            Object.values(nod)[13].innerHTML = (urlka.lst[11]);
            Object.values(nod)[14].innerHTML = (urlka.lst[12]);
            Object.values(nod)[15].innerHTML = (urlka.lst[13]);
            Object.values(nod)[16].innerHTML = (urlka.lst[14]);
            Object.values(nod)[17].innerHTML = (urlka.lst[15]);
            Object.values(nod)[19].innerHTML = (urlka.lst[16]);


            Refresh(nodeHeat);
            Refresh(nodeHist);
            $('#NahledImgHeat').removeAttr("hidden");
            $('#NahledImgHist').removeAttr("hidden");
        })
    }
    // Set the date we're counting down to
    var countDownDate = new Date()
    countDownDate = addMinutes(countDownDate, 60)
    countDownDate = countDownDate.getTime();

    // Update the count down every 1 second
    var xTimeout = setInterval(function () {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        // console.log(distance)
        if (distance < 0) {
            killSetTimout();
        }

        // Output the result in an element with id="demo"

    }, 1000);


    // added by dan - ajax loader modal
    $(".blueBorderInput").hover(function () {
        $("label[for='" + $(this).attr('id') + "']").toggleClass("blueBorderLabel");  //Toggle the active class to the area is hovered
    });

    $(document)
        .ajaxStart(function () {
            $('.loader').prop('hidden', false);
        })
        .ajaxStop(function () {
            $('.loader').prop('hidden', true);
        });
    $("#IDformPridajTM").on("submit", function (event) {
        event.preventDefault();
        var preslo = 1;
        let ltl = document.forms["formPridajTM"]["ltl"].value;
        let utl = document.forms["formPridajTM"]["utl"].value;
        if (parseInt(ltl) > parseInt(utl)) {
            if (!$('#utlLtlTR').length) {
                var t = 5000,
                    destination = 'LTL musí být nižší než UTL!',
                    div = $('<div />', { 'style': 'color: red; float: left;', text: destination, id: "utlLtlTR" });

                $('#pripojTRhranice').append(div);
                div.show(1).delay(t).hide(1, function () {
                    $(this).remove();
                });
            }
            preslo = 0
        }
        $(document).ready(function () {
            $('.loader').prop('hidden', false);
        })
        $.ajax({
            url: "/get_existTR",
            type: "POST",
            async: false,
            data: {
                "TreciMat": $("#TMNazov").val(),
                "typ": $("#DruhTMID").val(),

            },
            success: function (data) {
                if (data == "false") {
                    if (!$('#jeVDBTR').length) {
                        var t = 5000,
                            destination = 'Název pro daný typ je již v databázi!',
                            div = $('<div />', { 'style': 'color: red; float: left;', text: destination, id: "jeVDBTR" });

                        $('#pripojTRnazov').append(div);
                        div.show(1).delay(t).hide(1, function () {
                            $(this).remove();
                        });
                    }
                    preslo = 0

                }

            }
        })
        $(document).ready(function () {
            $('.loader').prop('hidden', true);
        })

        return Boolean(preslo);
    })
    $(document).ready(function () {
        $('#flexRadioDefault1').click((e) => {
            $('#NahledModalNastaveniePR').prop("disabled", false);
            $('#dateOfNahled').prop("disabled", true);
        });
        $('#flexRadioDefault2').click((e) => {
            $('#NahledModalNastaveniePR').prop("disabled", true);
            $('#dateOfNahled').prop("disabled", false);
        });
    });
    var dates;
    $(document).on('click', '.nacitajDates', function () {

        $.ajax({
            url: "/getDates",
            type: "POST",
            success: function (data) {
                dates = data;
                console.log(dates)
            },
        });
    });

    $("body").delegate("#dateOfNahled", "focusin", function () {
        $(this).datepicker({
            beforeShowDay: function (date) {
                var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
                return [dates.indexOf(string) != -1]
            }
        });
    });

    String.prototype.contains = function (findStr) {
        if (typeof findStr == typeof ['abc', 'def']) {
            var R = false;
            for (var i = 0; i < findStr.length; i++) {
                if (this.indexOf(findStr[i]) > -1) { R = true; break; }
            }
            return R;
        } else { return this.indexOf(findStr) > -1 ? true : false; }
    }
    function parseAjax(u, d = {}, callback) {
        // objekt d={} musí byť vyskladaný so stringových alebo číselných položiek, nezoberie klasický object v ktorom je napr. pole
        var ajaxStr = $.ajax({
            url: u, data: d, type: 'POST', /*async: false,*/ success: function (data) {
                //console.log("---ajax-success--"+u); console.log(data); 
                callback(data);
            }, error: function () { console.log("---ajax-error---" + u); }
        })
        // .responseText;
        // var res = null;
        // if (ajaxStr == undefined) { return }
        // if (ajaxStr.contains('{') || ajaxStr.contains('[')) {
        //     res = JSON.parse(ajaxStr)
        // } else { res = ajaxStr; }

        return false;
    }


    function Refresh(node) {
        let address;
        if (node.src.indexOf('?') > -1)
            address = node.src.split('?')[0];
        else
            address = node.src;
        node.src = address + "?time=" + new Date().getTime();

    }
    function ajaxInterval(druh) {

        // zenfunkcni inputy 
        // console.log("0");
        Iltl = parseFloat($('#ltlSPUSTIT').val());
        Iutl = parseFloat($('#utlSPUSTIT').val());
        i = 0;
        $(document).on('click', '#zmenLiveNahlad', function () {
            // console.log("som tu")
            if (i == 0) {
                i++;
                // console.log("click")
                Iltl = parseFloat($('#ltlSPUSTIT').val());
                Iutl = parseFloat($('#utlSPUSTIT').val());

                // console.log(Iltl + " " + Iutl)
                var els = document.getElementsByClassName("colorAble");
                // console.log(els);
                Array.prototype.forEach.call(els, function (el) {

                    hodnotaPolicka = parseFloat(el.dataset.value);

                    farba = zafarby(hodnotaPolicka, Iltl, Iutl)

                    el.style.backgroundColor = farba;
                    el.style.color = farba;


                })
                var els = document.getElementsByClassName("stats");
                // console.log(els);
                Array.prototype.forEach.call(els, function (el) {

                    hodnotaPolicka = parseFloat(el.textContent);

                    farba = zafarby(hodnotaPolicka, Iltl, Iutl)

                    el.style.backgroundColor = farba;


                })
            }
            // console.log("som von")
        });
        var prvyRiadok = document.getElementById("liveNahledBody").firstElementChild

        lID = prvyRiadok.getAttribute("id")
        lID = parseInt(lID)

        $.ajax({
            url: "/get_aktDataInterval",
            type: "POST",
            async: false,
            data: {
                "lastId": lID,
                "druh": druh,
            },
            success: function (data) {

                data.forEach(element => {

                    var el = $('<tr id="' + element.id + '">')
                    $("#liveNahledBody")
                        .prepend(el)
                    el.append($('<td class="dateFont">')
                        .text(element.name.slice(4, -3) + " ")
                    )
                    el.append($('<td class="dateFont stats" style="border: black solid;" >')
                        .text(" ")
                    )
                    el.append($('<td class="dateFont stats" style="border: black solid;">')
                        .text(" ")
                    )
                    el.append($('<td class="dateFont stats" style="border: black solid;">')
                        .text(" ")
                    )

                    for (let index = 0; index < element.data.length; index++) {
                        // console.log(element.data[index])
                        // console.log(typeof (element.name))

                        // console.log(Iltl + " " + Iutl)
                        farba = zafarby(element.data[index], Iltl, Iutl)
                        el.append($('<td class="colorAble" data-value="' + element.data[index] + '" style="background-color: ' + farba + ';color: ' + farba + ';padding: 10px 1px 5px 5px;" >.</td>'))

                    }

                    var tds = $('td.colorAble', el);
                    var values = tds.map(function () {
                        // console.log($(this).data('value'));
                        varr = $(this).data('value')
                        if (varr != 0) {
                            return +$(this).data('value'); // convert to number
                        }
                    }).get(); // convert to array
                    // Get the maximum value
                    var max = Math.max.apply(Math, values);
                    var min = Math.min.apply(Math, values);
                    if ((String(max)).indexOf('I') > -1) {
                        max = 0;
                    }
                    if ((String(min)).indexOf('I') > -1) {
                        min = 0;
                    }
                    function avgg(gradeData) {
                        const filtered = gradeData.filter(item => item !== 0);
                        if (filtered.length !== 0) {
                            const sum = filtered.reduce((a, b) => a + b);
                            const avg = sum / filtered.length;
                            // console.log(avg);
                            return avg.toFixed(2);
                        } else {
                            return 0;
                        }
                    }
                    // console.log(Iltl + " " + Iutl)
                    var mojeAvg = avgg(values);
                    farba1 = zafarby(max, Iltl, Iutl);
                    farba2 = zafarby(min, Iltl, Iutl);
                    farba3 = zafarby(mojeAvg, Iltl, Iutl);

                    $(el).children('td').eq(1).text(max.toFixed(2));
                    $(el).children('td').eq(1).css('background-color', farba1);
                    $(el).children('td').eq(2).text(min.toFixed(2));
                    $(el).children('td').eq(2).css('background-color', farba2);
                    $(el).children('td').eq(3).text(mojeAvg);
                    $(el).children('td').eq(3).css('background-color', farba3);
                    $('#headRow').removeClass('d-none');
                });


                $('#tdLTL').attr('value', ltl);
                $('#tdUTL').attr('value', utl);

            },
        });
        // console.log("1");
    }
    function zafarby(jsondata, par1, par2) {
        var Fltl = (isNaN(par1) ? 0 : par1)
        var Futl = (isNaN(par2) ? 0 : par2)
        seg = (Futl - Fltl) / 16
        if (jsondata < 0) { farba = "#000000"; }
        if (jsondata == 0) { farba = "#BFBFBF"; }


        if ((jsondata >= 0.0001) && (jsondata < Fltl)) { farba = "rgb(15, 182, 173)"; }

        if ((jsondata >= Fltl) && (jsondata < Fltl + 1 * seg)) { farba = "#FCFF3E"; }

        if ((jsondata >= Fltl + 1 * seg) && (jsondata < Fltl + 2 * seg)) { farba = "#E0EC37"; }


        if ((jsondata >= Fltl + 2 * seg) && (jsondata < Fltl + 3 * seg)) { farba = "#C3D92F"; }

        if ((jsondata >= Fltl + 3 * seg) && (jsondata < Fltl + 4 * seg)) { farba = "#A6C627"; }


        if ((jsondata >= Fltl + 4 * seg) && (jsondata < Fltl + 5 * seg)) { farba = "#89B31F"; }

        if ((jsondata >= Fltl + 5 * seg) && (jsondata < Fltl + 6 * seg)) { farba = "#6DA118"; }

        if ((jsondata >= Fltl + 6 * seg) && (jsondata < Fltl + 7 * seg)) { farba = "#42850D"; }

        if ((jsondata >= Fltl + 7 * seg) && (jsondata < Fltl + 8 * seg)) { farba = "#166801"; }

        if ((jsondata >= Fltl + 8 * seg) && (jsondata < Fltl + 9 * seg)) { farba = "#166801"; }

        if ((jsondata >= Fltl + 9 * seg) && (jsondata < Fltl + 10 * seg)) { farba = "rgb(66,133,13)"; }

        if ((jsondata >= Fltl + 10 * seg) && (jsondata < Fltl + 11 * seg)) { farba = "rgb(109,161,24)"; }

        if ((jsondata >= Fltl + 11 * seg) && (jsondata < Fltl + 12 * seg)) { farba = "rgb(155,146,28)"; }

        if ((jsondata >= Fltl + 12 * seg) && (jsondata < Fltl + 13 * seg)) { farba = "rgb(161,129,24)"; }

        if ((jsondata >= Fltl + 13 * seg) && (jsondata < Fltl + 14 * seg)) { farba = "rgb(161,102,24)"; }


        if ((jsondata >= Fltl + 14 * seg) && (jsondata < Fltl + 15 * seg)) { farba = "rgb(161,78,22)"; }

        if ((jsondata >= Fltl + 15 * seg) && (jsondata < Futl)) { farba = "rgb(161, 63, 24)"; }

        if ((jsondata >= Futl) && (jsondata < 1000000)) { farba = "#FF0000"; }//Number.MAX_SAFE_INTEGER
        return farba
    }
    $("#start").on("click", function () {
        let validitna = 1;
        let typ = $("#NahledModalNastavenieTyp").val();
        let ltl = parseFloat($("#ltl").val()); //438.9034;
        let utl = parseFloat($("#utl").val()); //474.8431
        if (ltl > utl) {
            if (!$('#utlLtlZlyPomer').length) {
                var t = 5000,
                    destination = 'LTL musí být nižší než UTL!',
                    div = $('<div />', { 'style': 'color: red; float: right;', text: destination, id: "utlLtlZlyPomer" });

                $('#pripojUTLLTL').append(div);
                div.show(1).delay(t).hide(1, function () {
                    $(this).remove();
                });
            }
            validitna = 0;
        }
        if ($("#flexRadioDefault1").prop("checked")) {

            let productionRun = $("#NahledModalNastaveniePR").val();
            let mString = String(productionRun);
            if (productionRun == '') {
                if (!$('#PrazdnyPRUN').length) {
                    var t = 5000,
                        destination = 'Zadejte Production run!',
                        div = $('<div />', { 'style': 'color: red; float: right;', text: destination, id: "PrazdnyPRUN" });

                    $('#pripoj').append(div);
                    div.show(1).delay(t).hide(1, function () {
                        $(this).remove();
                    });
                }
                validitna = 0;
            }
            else if (mString.indexOf('.') > -1) {
                if (!$('#BodkaPRUN').length) {
                    var t = 5000,
                        destination = 'Nie je možné používať "." pre Production run!',
                        div = $('<div />', { 'style': 'color: red;float: right;', text: destination, id: "BodkaPRUN" });

                    $('#pripoj').append(div);
                    div.show(1).delay(t).hide(1, function () {
                        $(this).remove();
                    });
                }
                validitna = 0;
            }
            if (validitna == 1) {
                prazdny = parseAjax("/get_existPRun", { 'productionRun': productionRun, 'typ': typ }, function (prazdny) {
                    if ((prazdny) === 'true') {
                        if (!$('#NotInDatabsPRUN').length) {
                            var t = 5000,
                                destination = 'Production run se nenachází v databázi!',
                                div = $('<div />', { 'style': 'color: red;float: right;', text: destination, id: 'NotInDatabsPRUN' });

                            $('#pripoj').append(div);
                            div.show(1).delay(t).hide(1, function () {
                                $(this).remove();
                            })
                        }
                        validitna = 0;
                    }
                })
            }

            if (validitna == 0) {
                return;
            }
            dajObrazok(productionRun, utl, ltl, typ);


        } else {

            datum = $("#dateOfNahled").val();
            if (datum == '') {
                if (!$('#PrazdnyDatum').length) {
                    var t = 5000,
                        destination = 'Zadejte Datum výroby!',
                        div = $('<div />', { 'style': 'color: red; float: right;', text: destination, id: "PrazdnyDatum" });

                    $('#pripojDatum').append(div);
                    div.show(1).delay(t).hide(1, function () {
                        $(this).remove();
                    });
                }
                validitna = 0;
            }


            if (validitna == 0) {
                return;
            }
            dajObrazok(datum, utl, ltl, typ);

        }

    });
    $("#getLiveNahlad").on("click", function () {
        $('.loader').prop('hidden', false);
        ltl = parseFloat($('#ltlSPUSTIT').val())
        utl = parseFloat($('#utlSPUSTIT').val())
        druhLive = $('#listTypovLive').val()
        $('.CgetLiveNahlad').addClass('d-none')
        $('.CzmenLiveNahlad').removeClass('d-none')
        $('.CgetLiveNahladTyp').prop('disabled', true);

        $.ajax({
            url: "/get_aktData",
            type: "post",
            async: false,
            data: {
                'druhLive': druhLive
            },
            success: function (data) {
                data.forEach(element => {
                    // data-value="'+druhLive+'"
                    var el = $('<tr id="' + element.id + '">')
                    $("#liveNahledBody").append(el)
                    el.append($('<td class="dateFont" >')
                        .text(element.name.slice(4, -3) + " ")
                    )
                    el.append($('<td class="dateFont stats" style="border: black solid;" >')
                        .text(" ")
                    )
                    el.append($('<td class="dateFont stats" style="border: black solid;">')
                        .text(" ")
                    )
                    el.append($('<td class="dateFont stats" style="border: black solid;">')
                        .text(" ")
                    )
                    for (let index = 0; index < element.data.length; index++) {
                        farba = zafarby(element.data[index], ltl, utl) //749, 815
                        el.append($('<td class="colorAble" data-value="' + element.data[index] + '" style="background-color: ' + farba + ';color: ' + farba + ';padding: 10px 1px 5px 5px;" >.</td>'))
                    }
                    var tds = $('td.colorAble', el);
                    var values = tds.map(function () {
                        // console.log($(this).data('value'));
                        varr = $(this).data('value')
                        if (varr != 0) {
                            return +$(this).data('value'); // convert to number
                        }
                    }).get(); // convert to array
                    // Get the maximum value
                    var max = Math.max.apply(Math, values);
                    var min = Math.min.apply(Math, values);
                    if ((String(max)).indexOf('I') > -1) {
                        max = 0;
                    }
                    if ((String(min)).indexOf('I') > -1) {
                        min = 0;
                    }
                    function avgg(gradeData) {
                        const filtered = gradeData.filter(item => item !== 0);
                        if (filtered.length !== 0) {
                            const sum = filtered.reduce((a, b) => a + b);
                            const avg = sum / filtered.length;
                            // console.log(avg);
                            return avg.toFixed(2);
                        } else {
                            return 0;
                        }
                    }
                    var mojeAvg = avgg(values);
                    farba1 = zafarby(max, ltl, utl);
                    farba2 = zafarby(min, ltl, utl);
                    farba3 = zafarby(mojeAvg, ltl, utl);

                    $(el).children('td').eq(1).text(max.toFixed(2));
                    $(el).children('td').eq(1).css('background-color', farba1);
                    $(el).children('td').eq(2).text(min.toFixed(2));
                    $(el).children('td').eq(2).css('background-color', farba2);
                    $(el).children('td').eq(3).text(mojeAvg);
                    $(el).children('td').eq(3).css('background-color', farba3);
                    $('#headRow').removeClass('d-none');
                });
                $('#tdLTL').attr('value', ltl);
                $('#tdUTL').attr('value', utl);
                $('.loader').prop('hidden', true);
                var hadle = setInterval(function () { ajaxInterval(druhLive); }, 5000);



            },
        });


    });
});



