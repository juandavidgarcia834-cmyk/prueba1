import re

import streamlit as st


def convertir_a_mayusculas(campo):
    st.session_state[campo] = st.session_state[campo].upper()


def sanitizar_nombre_ruta(campo):
    val = st.session_state.get(campo, "")
    st.session_state[campo] = re.sub(r"[^A-ZÁÉÍÓÚÑÜ0-9]", "", val.upper())


def validar_placa():
    _k = f"placa_vehiculo_{st.session_state.get('_ruta_fg', 0)}"
    if _k in st.session_state:
        st.session_state[_k] = re.sub(
            r"[^A-Z0-9]", "", st.session_state[_k].upper()
        )


def activar_siguiente_con_enter():
    if st.session_state.get("_nav_js_ok"):
        return
    st.session_state["_nav_js_ok"] = True
    st.html(
        """
        <script>
        (function(){
          if (window._navInstalled) return;
          window._navInstalled = true;

          var ST_FORM = [
            '[data-testid="stTextInput"]',
            '[data-testid="stNumberInput"]',
            '[data-testid="stDateInput"]',
            '[data-testid="stTimeInput"]',
            '[data-testid="stTextArea"]',
            '[data-testid="stSelectbox"]'
          ].join(',');

          function esFormInput(el) {
            return !!(el.closest && el.closest(ST_FORM));
          }
          function esSelectbox(el) {
            return !!(el.closest && el.closest('[data-testid="stSelectbox"]'));
          }
          function selectboxAbierto(el) {
            var c = el.closest('[data-testid="stSelectbox"]');
            if (!c) return false;
            return !!(c.querySelector('[class*="menu"]'));
          }
          function hayDataEditor() {
            var g = document.querySelector('[data-testid="stDataEditor"]');
            if (!g) return false;
            var r = g.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
          }

          // Devuelve el tab panel que contiene el elemento activo,
          // o el documento completo si no hay tabs activos.
          function getScopeDeEl(el) {
            if (!el || !el.closest) return document;
            var panel = el.closest('[data-testid="stTabPanel"]')
                     || el.closest('[role="tabpanel"]');
            return panel || document;
          }

          function clickBtnGuardar() {
            var scope = getScopeDeEl(document.activeElement);
            var vis = function(b) { return b.offsetParent !== null && b.innerText; };
            var btns = Array.from(scope.querySelectorAll('button'));
            var btn = btns.find(function(b) { return vis(b) && b.innerText.includes('AGREGAR MUESTRA'); })
                  || btns.find(function(b) { return vis(b) && b.innerText.includes('GUARDAR'); });
            if (btn) setTimeout(function() { btn.click(); }, 120);
          }

          function obtenerInputsVisibles() {
            var scope = getScopeDeEl(document.activeElement);
            return Array.from(scope.querySelectorAll('input,textarea')).filter(function(el) {
              if (!esFormInput(el)) return false;
              var t = el.getAttribute('type');
              if (t === 'hidden' || t === 'checkbox' || t === 'radio') return false;
              var r = el.getBoundingClientRect();
              return r.width > 0 && r.height > 0;
            });
          }

          function moverFoco(input, delta) {
            var todos = obtenerInputsVisibles();
            var pos = todos.indexOf(input);
            if (pos === -1) return;
            var dest = todos[pos + delta];
            if (dest) setTimeout(function() { dest.focus(); try { dest.select(); } catch(e) {} }, 60);
          }

          var _inGrid = false;

          document.addEventListener('focusin', function(e) {
            if (!_inGrid) return;
            var t = e.target, tag = t.tagName;
            if ((tag === 'INPUT' || tag === 'TEXTAREA') && !esFormInput(t)) return;
            if (tag === 'CANVAS' && t.closest('[data-testid="stDataEditor"]')) return;
            _inGrid = false; clickBtnGuardar();
          });

          document.addEventListener('keydown', function(e) {
            var a = document.activeElement;
            if (!a) return;
            var tag = a.tagName;
            if (tag !== 'INPUT' && tag !== 'TEXTAREA') return;

            if (esFormInput(a)) {
              var esSel = esSelectbox(a);
              if (esSel && selectboxAbierto(a)) return;

              var esNum = a.getAttribute('type') === 'number';
              var todos = obtenerInputsVisibles();
              var pos   = todos.indexOf(a);
              var esUlt = pos !== -1 && pos === todos.length - 1;
              var ph    = (a.placeholder || '').toLowerCase();

              if (e.key === 'Enter') {
                e.preventDefault(); e.stopPropagation();
                if (ph.includes('observaciones') || esUlt) clickBtnGuardar();
                else moverFoco(a, 1);
              } else if (e.key === 'ArrowRight' && !esSel && (esNum || a.selectionStart >= a.value.length)) {
                e.preventDefault(); e.stopPropagation(); moverFoco(a, 1);
              } else if (e.key === 'ArrowLeft' && !esSel && (esNum || a.selectionStart <= 0)) {
                e.preventDefault(); e.stopPropagation(); moverFoco(a, -1);
              }
              return;
            }

            if (!hayDataEditor()) return;
            var isNum = a.getAttribute('type') === 'number';
            var tab = function(sh) {
              a.dispatchEvent(new KeyboardEvent('keydown', {
                key: 'Tab', code: 'Tab', keyCode: 9, which: 9,
                shiftKey: !!sh, bubbles: true, cancelable: true, composed: true
              }));
            };
            if (e.key === 'Enter') {
              e.preventDefault(); e.stopPropagation(); _inGrid = true; tab(false);
            } else if (e.key === 'ArrowRight' && (isNum || a.selectionStart >= a.value.length)) {
              e.preventDefault(); e.stopPropagation(); tab(false);
            } else if (e.key === 'ArrowLeft' && (isNum || a.selectionStart <= 0)) {
              e.preventDefault(); e.stopPropagation(); tab(true);
            }
          }, true);
        })();
        </script>
        """,
        unsafe_allow_javascript=True,
    )
