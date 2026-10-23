document.addEventListener('DOMContentLoaded', function () {

    var TLDS = [
        '.com', '.in', '.co.in', '.org', '.net', '.edu', '.edu.in',
        '.ac.in', '.org.in', '.net.in', '.gov.in', '.info', '.co', '.io', '.me'
    ];

    var LIMITS = {
        name:   { max: 40, msg: 'Invalid: maximum 40 characters allowed' },
        mobile: { max: 10, msg: 'Invalid: only 10 digits allowed' },
        email:  { max: 100, msg: 'Invalid: maximum 100 characters allowed' }
    };

    var rules = {
        name: function (v, final) {
            if (!/^[A-Za-z .]*$/.test(v)) return 'Invalid: only letters, spaces and dots allowed';
            if (final && v.length > 0 && v.length < 3) return 'Invalid: minimum 3 characters';
            return '';
        },

        mobile: function (v) {
            if (v === '') return '';
            if (!/^\d*$/.test(v)) return 'Invalid: digits only';
            if (!/^[6-9]/.test(v)) return 'Invalid: Indian mobile must start with 6, 7, 8 or 9';
            if (v.length < 10) return 'Invalid: enter all 10 digits (now ' + v.length + ')';
            return '';
        },

        email: function (v) {
            v = v.toLowerCase();
            if (v === '') return '';
            if (!/^[a-z0-9._%+-]+@[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(v) || v.indexOf('..') !== -1) {
                return 'Invalid email address';
            }
            var ok = TLDS.some(function (t) { return v.endsWith(t); });
            return ok ? '' : 'Invalid: use an ending like .com, .in, .org or .edu';
        }
    };

    var checks = [];

    document.querySelectorAll('[data-validate]').forEach(function (input) {
        var type = input.getAttribute('data-validate');
        if (!rules[type]) return;

        input.removeAttribute('maxlength');

        var msg = document.createElement('p');
        msg.className = 'form-inline-error';
        msg.setAttribute('role', 'alert');
        input.insertAdjacentElement('afterend', msg);

        function show(err) {
            msg.textContent = err;
            input.classList.toggle('form-invalid', err !== '');
        }

        function check(final) {
            var err = rules[type](input.value.trim(), final);
            show(err);
            input.setCustomValidity(err);
            return err === '';
        }

        input.addEventListener('input', function () {
            var limit = LIMITS[type];
            var hitLimit = false;

            if (limit && input.value.length > limit.max) {
                input.value = input.value.slice(0, limit.max);
                hitLimit = true;
            }

            var ok = check(false);
            if (hitLimit && ok) show(limit.msg);
        });

        input.addEventListener('blur', function () { check(true); });
        checks.push(function () { return check(true); });
    });

    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            var allOk = true;
            checks.forEach(function (run) { if (!run()) allOk = false; });
            if (!allOk) e.preventDefault();
        });
    });
});