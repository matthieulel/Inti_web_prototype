
$(document).ready(function(){

  //Show Modal si pas de record dans localstorage
  if (localStorage.getItem('landingmodal') !== null) {
    console.log(localStorage.getItem('landingmodal'))
  } else {
    $("#modalnewuser").modal('show');
  }



  // Init icons ---> sortir du doc.ready si effet de bord
  (function () {
    'use strict'
    feather.replace()

    $("#table_information").hide()
    $("#table_monitoring").hide()
    $('#expert_menu').hide()
    $('#sdo_date').hide();
    $('#sdo_time').hide();
    $('#mypic_title').hide();
    $('#sdopic_title').hide();
    $("#loader_text").hide();

    //$('#expertmode').attr("checked", ' ');
    $('#expertmode').removeAttr("checked", ' ');
    $('#sdocomp').removeAttr("checked", ' ');

    var user_settings ;

    if (localStorage.getItem('workspace') !== null) {
      user_settings = true
      console.log(localStorage.getItem('workspace'))
      //$('input.workspace_value').val(localStorage.getItem('workspace'));
      $('#workspace_name').val(localStorage.getItem('workspace'));
      $("#setPathBtn").removeClass('btn-danger')
      $("#setPathBtn").addClass('btn-success')
    } else {
      user_settings = false
      console.log(user_settings)
    }


  })();


});// end of doc.ready


// ---------- ONLY FOR TEST HERE -------

console.log('Get du workspace name' + $("#workspace_name").val())




// --------- END TEST ------------




// user variables
// TODO : LocalStorage ?
var workspace = "";
var ser_filename ="";

var picture_processed_log = {};
var is_expert_mode = false;
var is_sdo = false;




function set_modal_settings(){

  localStorage.setItem('landingmodal', false)

}






// Checkbox Mode expert
$(document).on('click','#expertmode',function(e){
  if($(this).is(':checked')){

    ///// Show expert menu
    $('#expert_menu').show();
    is_expert_mode = true;
    console.log(' good');

  }
  else {
    $('#expert_menu').hide();
    is_expert_mode = false;
    console.log('not good')
  }  
});



// Checkbox SDO
$(document).on('click','#sdocomp',function(e){
  if($(this).is(':checked')){
    is_sdo = true;
    $('#sdo_date').show();
    $('#sdo_time').show();
    showSnackbar('sdoToast')
    console.log('SDO activate')

  }
  else {
    is_sdo = false;
    $('#sdo_date').hide();
    $('#sdo_time').hide();
    console.log('SDO NOT activate')
  }  
});



/**
$(document).ready(function () {

  $("#nanogallery2").nanogallery2( {
      // ### gallery settings ### 
      thumbnailHeight:  150,
      thumbnailWidth:   150,
      itemsBaseURL:     'static/uploads/',
      
      // ### gallery content ### 
      items: [
          { src: 'Capture 2021-06-12T15_31_04Z_disk.png', srct: 'Capture 2021-06-12T15_31_04Z_disk.png', title: 'Berlin 1' },
          { src: 'berlin2.jpg', srct: 'berlin2_t.jpg', title: 'Berlin 2' },
          { src: 'berlin3.jpg', srct: 'berlin3_t.jpg', title: 'Berlin 3' }
        ]
    });
});

**/









// Btn Valider Workspace -> si valide -> Vert
$("#setPathBtn").click(function(){
  if(0 === $("#workspace_name").val().length){
    alert("Type folder name please.");
  }
  else{
    workspace = $("#workspace_name").val();
    $("#setPathBtn").removeClass('btn-danger')
    $("#setPathBtn").addClass('btn-success')

    localStorage.setItem('workspace', $("#workspace_name").val());

    // TODO : Regex verif présence du / en premier -> alias docker


  }
});

// Si modification du champs Folder -> Btn Valider -> red
$("#workspace_name" ).on( "input", function() {
  console.log("OK MAN");
  $("#setPathBtn").removeClass('btn-success')
  $("#setPathBtn").addClass('btn-danger')
});




function get_nb_ser_in_folder(){

  //récupération du champs folder TODO : ajout de vérifications -> ajout d'une méthode (voir mass process)
  workspace =  $("#workspace_name").val()


  var file_info = {
    folder : workspace,
    ser : ser_filename
  }

  

    $.ajax({
      type : 'POST',
      url : "/nbserfiles",
      dataType: 'json',
      contentType: 'application/json',
      data : JSON.stringify(file_info),
    
      success: function(response) {
        console.log(response);
        $('#ser_files_founded').empty();
        $('#ser_files_founded').append('Nombre de fichiers à traiter : ' + response);
    },   

    error: function(error) {
        console.log(error);
    }
    });


}






// Lancement du process de traitement par lot en Ajax
// Route : /massprocess
function mass_process(){

    //récupération du champs folder TODO : ajout de vérifications -> ajout d'une méthode (voir mass process)
    workspace =  $("#workspace_name").val()


    var file_info = {
      folder : workspace,
      ser : ser_filename
    }

    

      $.ajax({
        type : 'POST',
        url : "/massprocess",
        dataType: 'json',
        contentType: 'application/json',
        data : JSON.stringify(file_info),
        beforeSend: function () {
        // Affichage du loader pour users
        $("#loader").attr("src", 'static/ajax-loader.gif');
        $("#loader_text").show();
    },
        success: function(response) {
          // Suppression du loader
          $("#loader").attr("src", '');
          $("#loader_text").hide();

          $.each(response, function(i, obj) {


            $('#mass_gallery').append( "<a href = " + obj.imgsrc + " data-ngThumb = " + obj.imgsrc + "> "+ obj.imgsrc + "</a>");
          
          });

          // TODO -> Si retour OK -> Affichage user

          $("#mass_gallery").nanogallery2( {
            // ### gallery settings ### 
        
            itemsBaseURL:     'static/uploads/',
            thumbnailHeight:  800,
            thumbnailWidth:   600,
          });

          console.log(response);

      },   

      error: function(error) {
          console.log(error);
      }
      });
  }


//Affichage de la galerie principale
function show_single_gallery(srcImg, srcInvertImg){


  $("#nanogallery2").nanogallery2( {
    // ### gallery settings ### 

    itemsBaseURL:     'static/uploads/',
    thumbnailHeight:  400,
    thumbnailWidth:   600,
    
    // ### gallery content ### 
    items: [
        { src: srcImg, srct: srcImg, title: srcImg},
        { src: srcInvertImg, srct: srcInvertImg, title: srcInvertImg}

      ]
  });
}


function show_sdo_gallery(splitElement, splitElement2) {

    $("#sdogallery").nanogallery2( {
    // ### gallery settings ###

    itemsBaseURL:     'static/uploads/',
    thumbnailHeight:  400,
    thumbnailWidth:   600,

    // ### gallery content ###
    items: [
        { src: splitElement, srct: splitElement, title: splitElement + ' Crédit : SDO - HMIB'},
        { src: splitElement2, srct: splitElement2, title: splitElement2 + ' Crédit : SDO - HMIB'}
      ]
  });

  $('#mypic_title').show();
  $('#sdopic_title').show();

}




// Lancement du process .SER unique en ajax
function single_process(){

  //récupération du champs folder TODO : ajout de vérifications -> ajout d'une méthode (voir mass process)
  workspace =  $("#workspace_name").val()
  //ser_filename =  $("#ser_filename").val()
  // le préfixe C:\\fakepath est ajouté par certains navigateur par sécurité
  //TODO : test à prévoir avec tous les navigateurs courants (Firefox OK, Chrome OK, Edge ?)
  console.log($("#ser_filename").val().split('C:\\fakepath\\')[1])
  ser_filename = $("#ser_filename").val().split('C:\\fakepath\\')[1]


  var file_info = {
    folder : workspace,
    ser : ser_filename
  }

  if(is_sdo == true) {
      file_info['sdo'] = 1;
      file_info['sdo_date'] = $('#sdo_date').val();
      file_info['sdo_time'] = $('#sdo_time').val();
      console.log(file_info['sdo_date'])
      console.log(file_info['sdo_time'])
  }
   else {
      file_info['sdo'] = 0
  }


  // Envoi du nom du fichier pour traitement
  $.ajax({
    type : 'POST',
    url : "/",
    dataType: 'json',
    contentType: 'application/json',
    data : JSON.stringify(file_info),
    beforeSend: function () {
        $('#mypic_title').hide()
        $('#sdopic_title').hide()
        $('#nanogallery2').hide()
        $('#sdogallery').hide()
        $("#table_information").hide()
      // Affichage du loader pour users
      $("#loader").attr("src", 'static/ajax-loader.gif');
      $("#loader_text").show();
      
  },
  success: function(response) {

    $('#mypic_title').show()
    $('#sdopic_title').show()
    $('#nanogallery2').show()
    $('#sdogallery').show()

   // Suppression du loader
    $("#loader").attr("src", '');
    $("#loader_text").hide();

   $("#table_information").show()

   //GALLERY
   show_single_gallery(response['imgsrc'].split('static/uploads/')[1], response['invert_imgsrc'].split('static/uploads/')[1])
   if(is_sdo){
       show_sdo_gallery(response['hmib'].split('static/uploads/')[1], response['hmiif'].split('static/uploads/')[1])
   }
   else{
    $('#sdopic_title').hide()
    $('#sdogallery').hide();
   }




    // fill single process log tab
    picture_processed_log['filetodownload'] = response['imgsrc'].split('static/uploads/')[1];
    picture_processed_log['serfilename'] = response['imgser'];
    picture_processed_log['ziptodownload'] = response['zip_path'].split('static/uploads/')[1];
    picture_processed_log['nbframe'] = response['nb de frame '];
    picture_processed_log['vert_limit'] = response['Limites verticales y1,y2 '];
    picture_processed_log['horiz_limit'] = response['Limites horizontales x1, x2 '];
    picture_processed_log['coeffa'] = response['Coef A0,A1,A2 '];
    picture_processed_log['axesy'] = response['Axe y_x1, y_x2 '];
    picture_processed_log['centercercle'] = response['Centre cercle x0,y0 et diamètre '];
    picture_processed_log['ratiosysx'] = response['Ratio SY/SX '];
    picture_processed_log['slant'] = response['Angle slant'];
    picture_processed_log['src'] = response['imgsrc'];
    picture_processed_log['src_invert'] = response['invert_imgsrc'];


    // set value in tab
    $("#filedwn").html(response['imgsrc'].split('static/uploads/')[1]);
    $("#serfilename").html(response['imgser']);
    $("#zipdwn").html(response['zip_path'].split('static/uploads/')[1]);
    $("#nbframe").html(response['nb de frame ']);
    $("#vert_limit").html(response['Limites verticales y1,y2 ']);
    $("#horiz_limit").html(response['Limites horizontales x1, x2 ']);
    $("#coeffa").html(response['Coef A0,A1,A2 ']);
    $("#axesy").html(response['Axe y_x1, y_x2 ']);
    $("#centercercle").html(response['Centre cercle x0,y0 et diamètre ']);
    $("#ratiosysx").html(response['Ratio SY/SX ']);
    $("#slant").html(response['Angle slant']);

    
    // affichage de l'image 
    //---------------------> $("#result_image").attr("src", response['imgsrc']);
    // lien de téléchargement de l'image et du fichier zip
    $("#filedwn").attr("href", response['imgsrc']);
    $("#zipdwn").attr("href", response['zip_path']);
  },
    error: function(error) {
       console.log(error);
    }
  });
}



function copy(elem){

  console.log(picture_processed_log[String(elem.id.split('_btn')[0])])
    navigator.clipboard.writeText(picture_processed_log[String(elem.id.split('_btn')[0])]).then(function() {
      /* clipboard successfully set */
      //console.log('ok')
      showSnackbar('copyToast')

    }, function() {
      /* clipboard write failed */
      alert("Erreur durant la copie - Veuillez recommencer")
    });

}



function showSnackbar(idToShow){
    console.log(idToShow)
  //$('#liveToast').toast('show');
    $('#'+idToShow).toast('show');
  setTimeout(function(){ $('#'+idToShow).toast('hide'); }, 10000);
}







// Lancement du process de traitement par lot en Ajax
// Route : /massprocess
function launch_watching(){

  //récupération du champs folder TODO : ajout de vérifications -> ajout d'une méthode (voir mass process)
  workspace =  $("#workspace_name").val()



        var file_info = {
          folder : workspace,
        }

        $.ajax({
          type : 'POST',
          url : "/monitor",
          dataType: 'json',
          contentType: 'application/json',
          data : JSON.stringify(file_info),
          beforeSend: function () {
          // Affichage du loader pour users

          },
          success: function(response) {
            // Suppression du loader
   
            console.log('OK launched')

            console.log(response);
            if(response == 'on'){
              console.log('OK on est sur on');

              $("#loader").attr("src", 'static/1492.gif');
              $("#loader_text").show();
    

              $("#monitor_launcher").addClass('btn-danger');
              $("#monitor_launcher").removeClass('btn-outline-secondary');
              $("#monitor_launcher").html('Stopper la surveillance'); 


              // boucle toutes les 5 secondes pour vérifier le contenu du dossier en surveillance
              timer = setInterval(function() {
                console.log(get_monitor_state());
              }, 10000);


             
              
            





            }
            else if(response == 'off'){
              console.log('NOK on est sur Off')
              $("#monitor_launcher").html('Lancer la surveillance'); 
              $("#monitor_launcher").removeClass('btn-danger');
              $("#monitor_launcher").addClass('btn-outline-secondary');
              $("#loader").attr("src", '');
              $("#loader_text").hide();
              $("#table_monitoring").hide()
              clearTimeout(timer)
            }

        },   

        error: function(error) {
            console.log(error);
        }
        });


  }




// Retourne le nombre de fichiers ser/png et l'état de la surveillance true/false -> utilisé pour démarrer arreter le service

function get_monitor_state(){


  //récupération du champs folder TODO : ajout de vérifications -> ajout d'une méthode (voir mass process)
  workspace =  $("#workspace_name").val()

  var file_info = {
    folder : workspace,
  }

    $.ajax({
      type : 'POST',
      url : "/getmonitorstate",
      dataType: 'json',
      contentType: 'application/json',
      data : JSON.stringify(file_info),
      beforeSend: function () {
      // Affichage du loader pour users
      },
      success: function(response) {
        console.log(response)
        $('#monitoring_state').html('<h5>État du dossier surveillé</h5>')
        $("#table_monitoring").show()
        $("#ser_monitored").html(response[0]);
        $("#png_monitored").html(response[1]);
        $("#is_monitoring").html(response[2]);
        console.log(response[1] )
        console.log(response[0])
        if( !(response[1] / response[0] == 2) || (response[0] > 0 && response[1] == 0)){
          $('#is_in_process').html('true')
        }
        else{
          $('#is_in_process').html('false')
        }
        
    },   

    error: function(error) {
        console.log(error);
   
    }
    });

}