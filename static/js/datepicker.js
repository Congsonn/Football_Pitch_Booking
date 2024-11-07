const default_options = {
  autohide: true,
  format: "dd-mm-yyyy",
  orientation: "top",
  clearBtn: true,
  todayBtn: true,
  todayBtnMode: 1,
  weekStart: 1,
  language: "vi",
};

function initDatepicker(id, additional_options = null) {
  const $elm = document.getElementById(id);
  let options = default_options;

  if (!$elm) return;

  if (additional_options) {
    options = { ...default_options, ...additional_options };
  }
  new Datepicker($elm, options);
}
