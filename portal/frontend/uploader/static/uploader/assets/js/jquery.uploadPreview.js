(function ($) {
  $.extend({
    uploadPreview : function (extra) {

      // Options + Defaults
      var settings = [{
        input_field: ".image-input",
        preview_box: ".image-preview",
        label_field: ".image-label",
        label_default: "Choose File",
        label_selected: "Change File",
        no_label: false,
        success_callback : null,
      }];
      console.log(extra);
      settings = extra;
      /*if(extra.length > 1){
        settings = extra;
      }
      else if(extra.length == 1){

      }*/
      console.log(settings);

      // Check if FileReader is available
      if (window.File && window.FileList && window.FileReader) {
        $.each(settings,function(i,item){
        if (typeof($(item.input_field)) !== 'undefined' && $(item.input_field) !== null) {
          $(item.input_field).change(function() {
            var files = this.files;

            if (files.length > 0) {
              var file = files[0];
              var reader = new FileReader();

              // Load file
              reader.addEventListener("load",function(event) {
                var loadedFile = event.target;
                var image = new Image();
                image.src =  loadedFile.result;
                image.onload = function(){
                    console.log(this.height);
                };

                var height = (600/image.width)*image.height;
                console.log(height);
                $('#canvas1').css("top",(480-height)/2 + "px");

                // Check format
                if (file.type.match('image')) {

                  // Image


                  if(1){
                  $(item.preview_box).css("background-image", "url("+loadedFile.result+")");
                  $(item.preview_box).css("background-size", "contain");
                  $(item.preview_box).css("background-position", "center center");
                  $(item.preview_box).css("background-repeat", "no-repeat");
                  }
                  else{
                  console.log('yay');
                    $(item.preview_box).html('<img src=' + loadedFile.result + ' style="max-width:100%;margin:auto 0px;">')
                  }

                } else if (file.type.match('audio')) {
                  // Audio
                  $(item.preview_box).html("<audio controls><source src='" + loadedFile.result + "' type='" + file.type + "' />Your browser does not support the audio element.</audio>");
                } else {
                  alert("This file type is not supported yet.");
                }
              });

              if (item.no_label == false) {
                // Change label
                $(item.label_field).html(item.label_selected);
              }

              // Read the file
              reader.readAsDataURL(file);

              // Success callback function call
              if(!item.success_callback) {
                item.success_callback();
              }
            } else {
              if (item.no_label == false) {
                // Change label
                $(item.label_field).html(item.label_default);
              }

              // Clear background
              $(item.preview_box).css("background-image", "none");

              // Remove Audio
              $(item.preview_box + " audio").remove();
            }
          });
        }});
      } else {
        alert("You need a browser with file reader support, to use this form properly.");
        return false;
      }
    }
  });
})(jQuery);
