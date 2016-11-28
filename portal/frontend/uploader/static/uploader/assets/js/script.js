$(document).ready(function() {
  $.uploadPreview([{
    input_field: "#inputfile1",   // Default: .image-upload
    preview_box: "#abc1",  // Default: .image-preview
    label_field: "#image-label",    // Default: .image-label
    label_default: "Choose File",   // Default: Choose File
    label_selected: "Change File",  // Default: Change File
    no_label: true                 // Default: false
  },{
    input_field: "#inputfile2",   // Default: .image-upload
    preview_box: "#abc2",  // Default: .image-preview
    label_field: "#image-label",    // Default: .image-label
    label_default: "Choose File",   // Default: Choose File
    label_selected: "Change File",  // Default: Change File
    no_label: true                 // Default: false
  }]);

  $('#x1').click(function(){
        $('#inputfile1').click()
  });

  $('#x2').click(function(){
        $('#inputfile2').click()
  });

  console.log($(".drop").innerWidth());
});