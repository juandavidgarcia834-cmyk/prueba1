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
    # Sin guard de Python: st.html() se renderiza en CADA render para que
    # el árbol de widgets sea estable entre reruns (un st.html() ausente
    # desplaza las claves auto-generadas de todos los widgets siguientes,
    # incluyendo st.tabs(), lo que causa que React los remonte y reinicie al tab 0).
    # El guard JavaScript (window._navInstalled) impide listeners duplicados.
    st.html(
        """
        <script>
        (function(){
          if (window._navInstalled) return;
          window._navInstalled = true;

          /* ── Selectores de widgets Streamlit ─────────────────────── */
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

          /* ── Visibilidad real del elemento ───────────────────────── */
          function esVisible(el) {
            if (el.offsetParent === null) return false;
            var cs = window.getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') return false;
            var r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
          }

          /* ── Botón GUARDAR dentro del panel activo ───────────────── */
          function clickBtnGuardar() {
            var vis = function(b) {
              if (!b.innerText) return false;
              if (b.offsetParent === null) return false;
              var cs = window.getComputedStyle(b);
              if (cs.display === 'none' || cs.visibility === 'hidden') return false;
              var r = b.getBoundingClientRect();
              return r.width > 0 && r.height > 0;
            };
            var btns = Array.from(document.querySelectorAll('button'));
            var btn = btns.find(function(b) { return vis(b) && b.innerText.includes('AGREGAR MUESTRA'); })
                  || btns.find(function(b) { return vis(b) && b.innerText.includes('GUARDAR'); })
                  || btns.find(function(b) { return vis(b) && b.innerText.toUpperCase().includes('INICIAR SESI'); });
            if (btn) setTimeout(function() { btn.click(); }, 120);
          }

          /* ── Inputs visibles en la página ────────────────────────── */
          function obtenerInputsVisibles() {
            return Array.from(document.querySelectorAll('input,textarea')).filter(function(el) {
              if (!esFormInput(el)) return false;
              var t = el.getAttribute('type');
              if (t === 'hidden' || t === 'checkbox' || t === 'radio') return false;
              return esVisible(el);
            });
          }

          function moverFoco(input, delta) {
            var todos = obtenerInputsVisibles();
            var pos = todos.indexOf(input);
            if (pos === -1) return;
            var dest = todos[pos + delta];
            if (dest) setTimeout(function() { dest.focus(); try { dest.select(); } catch(e) {} }, 60);
          }

          /* ══════════════════════════════════════════════════════════
             PRESERVACIÓN DE TAB ACTIVO ENTRE RERUNS DE STREAMLIT
             ──────────────────────────────────────────────────────────
             st.tabs() reinicia al tab 0 en cada rerun de Streamlit.
             Guardamos el tab activo en sessionStorage y lo restauramos
             automáticamente después de cada rerun via MutationObserver.
          ══════════════════════════════════════════════════════════ */
          var _qlTabKey    = '_ql_seg_tab';
          var _qlRestTimer = null;
          var _qlLocked    = false;   // evita restauraciones re-entrantes

          function _qlGetSegTabs() {
            /* Busca el grupo de tabs de SEGUIMIENTOS por sus etiquetas */
            var all = Array.from(document.querySelectorAll('[data-testid="stTab"]'));
            for (var i = 0; i < all.length; i++) {
              var txt = (all[i].textContent || '').toUpperCase();
              if (txt.includes('ESTACIONES') || txt.includes('ACOMP') || txt.includes('CONTRA')) {
                /* Encontramos el primer tab del grupo; recogemos el contenedor */
                var wrap = all[i].closest('[data-baseweb="tab-list"]')
                        || all[i].closest('[role="tablist"]')
                        || all[i].parentElement;
                if (!wrap) return [];
                return Array.from(wrap.querySelectorAll('[data-testid="stTab"]'));
              }
            }
            return [];
          }

          function _qlActiveIdx(tabs) {
            for (var i = 0; i < tabs.length; i++) {
              if (tabs[i].getAttribute('aria-selected') === 'true') return i;
            }
            return 0;
          }

          function _qlSaveTab() {
            var tabs = _qlGetSegTabs();
            if (!tabs.length) return;
            var idx = _qlActiveIdx(tabs);
            sessionStorage.setItem(_qlTabKey, String(idx));
          }

          function _qlRestoreTab() {
            if (_qlLocked) return;
            var saved = sessionStorage.getItem(_qlTabKey);
            if (saved === null) return;
            var idx = parseInt(saved, 10);
            if (idx === 0) return;          /* tab 0 es el default, no hace falta restaurar */
            var tabs = _qlGetSegTabs();
            if (!tabs.length || idx >= tabs.length) return;
            var current = _qlActiveIdx(tabs);
            if (current === idx) return;    /* ya estamos en el tab correcto */
            _qlLocked = true;
            tabs[idx].click();
            setTimeout(function() { _qlLocked = false; }, 600);
          }

          /* Escuchar clics de usuario en los tabs → guardar índice */
          document.addEventListener('click', function(e) {
            if (!e.target || !e.target.closest) return;
            var tab = e.target.closest('[data-testid="stTab"]');
            if (tab) setTimeout(_qlSaveTab, 80);   /* esperar a que React actualice aria-selected */
          }, true);

          /* MutationObserver: detectar reruns de Streamlit y restaurar tab */
          var _qlObserver = new MutationObserver(function() {
            clearTimeout(_qlRestTimer);
            _qlRestTimer = setTimeout(_qlRestoreTab, 200);
          });
          _qlObserver.observe(document.body, { childList: true, subtree: true });

          /* ── Manejo de Data Editor (grilla) ──────────────────────── */
          var _inGrid = false;

          document.addEventListener('focusin', function(e) {
            if (!_inGrid) return;
            var t = e.target, tag = t.tagName;
            if ((tag === 'INPUT' || tag === 'TEXTAREA') && !esFormInput(t)) return;
            if (tag === 'CANVAS' && t.closest('[data-testid="stDataEditor"]')) return;
            _inGrid = false; clickBtnGuardar();
          });

          /* ── Navegación por teclado ───────────────────────────────── */
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
        """
    )
