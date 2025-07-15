$(document).ready(function () {

  // Load divisions on province change
  $('#sourceProvince').change(function () {
    const province = $(this).val();
    $('#sourceDivision').html('<option value="">Loading...</option>');
    $('#sourceDistrict').html('<option value="">Select Division First</option>');

    $.get(`/form/get_divisions/${province}`, function (divisions) {
      let options = '<option value="">Select Division</option>';
      divisions.forEach(division => {
        options += `<option value="${division}">${division}</option>`;
      });
      $('#sourceDivision').html(options);
    });
  });

  // Load districts on division change
  $('#sourceDivision').change(function () {
    const province = $('#sourceProvince').val();
    const division = $(this).val();

    $('#sourceDistrict').html('<option value="">Loading...</option>');
    $.get(`/form/get_districts/${province}/${division}`, function (districts) {
      let options = '<option value="">Select District</option>';
      districts.forEach(district => {
        options += `<option value="${district}">${district}</option>`;
      });
      $('#sourceDistrict').html(options);
    });
  });

  // Load destinations on destination province change
  $('#destProvince').change(function () {
    const province = $(this).val();
    $('#destination').html('<option value="">Loading...</option>');

    $.get(`/form/get_destinations/${province}`, function (destinations) {
      let options = '<option value="">Select Destination</option>';
      destinations.forEach(dest => {
        options += `<option value="${dest}">${dest}</option>`;
      });
      $('#destination').html(options);
    });
  });

  // Auto-fetch fare
  $('#sourceDistrict, #destination, #mode').change(function () {
    const source = $('#sourceDistrict').val();
    const destination = $('#destination').val();
    const mode = $('#mode').val();

    if (source && destination && mode) {
      $.ajax({
        url: '/form/get_fare',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ source, destination, mode }),
        success: function (data) {
          $('#fare').val(data.fare);
        },
        error: function () {
          $('#fare').val("Fare not found");
        }
      });
    }
  });

  // Submit form
  $('#travelForm').submit(function (e) {
    e.preventDefault();

    const data = {
      name: $('input[name="name"]').val(),
      sourceProvince: $('#sourceProvince').val(),
      sourceDivision: $('#sourceDivision').val(),
      sourceDistrict: $('#sourceDistrict').val(),
      destProvince: $('#destProvince').val(),
      destination: $('#destination').val(),
      mode: $('#mode').val(),
      fare: $('#fare').val()
    };

    $.ajax({
      url: '/form/submit',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function (response) {
        $('#travelForm').hide();

        const summaryHtml = `
          <div class="form-summary" id="summaryToPrint">
            <h2>Form Submitted Successfully</h2>
            <p><strong>Name:</strong> ${data.name}</p>
            <p><strong>Source:</strong> ${data.sourceDistrict}, ${data.sourceDivision}, ${data.sourceProvince}</p>
            <p><strong>Destination:</strong> ${data.destination}, ${data.destProvince}</p>
            <p><strong>Travel Mode:</strong> ${data.mode}</p>
            <p><strong>Fare:</strong> Rs. ${data.fare}</p>
            <p class="developer-credit">National Travel system developed by Abdullah Abid</p>
            <button id="downloadPdf" class="btn">Download PDF</button>
          </div>
        `;

        $('.form-section').append(summaryHtml);
        $('.form-summary').css({
          backgroundColor: '#d4edda',
          padding: '30px',
          borderRadius: '12px',
          boxShadow: '0 4px 20px rgba(0, 128, 0, 0.2)',
          marginTop: '30px',
          color: '#155724'
        });

        $('.form-summary h2').css({
          fontSize: '1.8rem',
          marginBottom: '20px'
        });

        $('.form-summary p').css({
          marginBottom: '10px',
          fontSize: '1.1rem'
        });

      $('#downloadPdf').click(function() {
    const { jsPDF } = window.jspdf;
    const summaryElement = $('#summaryToPrint');
    const downloadButton = $(this);

    // PDF banane se pehle, button ko chupayen aur naya style lagayein
    downloadButton.hide();
    summaryElement.addClass('pdf-view');

    html2canvas(summaryElement[0], { // html2canvas ko DOM element chahiye, isliye [0]
        scale: 2 // Behtar quality ke liye resolution barhayein
    }).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
        
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('Travel_Booking_Details.pdf');
        
        // PDF banne ke baad, naya style hatayein aur button wapis dikhayein
        summaryElement.removeClass('pdf-view');
        downloadButton.show();
    });
});
      }
    });
  });
});
