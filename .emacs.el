(set-language-environment "UTF-8")

(setq custom-file "~/.emacs.d/.emacs-custom.el")
(load custom-file)

(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)
(column-number-mode t)


;; Espace reserve aux macro

(fset 'initC
   [?# ?i ?n ?c ?l ?u ?d ?e ?  ?< ?s ?t ?d ?i ?o ?. ?h ?> return return kp-divide kp-multiply ?  ?L ?e ?s ?  ?s ?t ?r ?u ?c ?t ?u ?r ?e ?s ?  ?\\ ?s ?  kp-multiply kp-divide return return return return kp-divide kp-multiply ?  ?L ?e ?s ?  ?f ?o ?n ?c ?t ?i ?o ?n ?  ?\\ ?f ?  kp-multiply kp-divide return return return return kp-divide kp-multiply ?  ?L ?e ?  ?m ?a ?i ?n ?  ?\\ ?m ?  kp-multiply kp-divide return return ?i ?n ?t ?  ?m ?a ?i ?n ?\( ?\) ?\{ return return return ?r ?e ?t ?u ?r ?n ?  kp-0 ?\; return ?\}])

;; Fin de l'espace reserve aux macro

(setq python-shell-interpreter "python3")

(setq truncate-partial-width-windows nil)
(setq ring-bell-function 'ignore)
(display-time-mode t)

(global-set-key (kbd "C-c c") 'compile)
(global-set-key (kbd "C-c h") 'replace-string)

;; INSTALL PACKAGES
;; --------------------------------------

(require 'package)
(add-to-list 'package-archives
             '("elpy" . "http://jorgenschaefer.github.io/packages/"))

(add-to-list 'package-archives
       '("melpa" . "http://melpa.org/packages/") t)

(package-initialize)
(when (not package-archive-contents)
  (package-refresh-contents))

(defvar myPackages
  '(better-defaults
    elpy
    flycheck
    material-theme))

(elpy-enable)


(mapc #'(lambda (package)
    (unless (package-installed-p package)
      (package-install package)))
      myPackages)

;; BASIC CUSTOMIZATION
;; --------------------------------------

(setq inhibit-startup-message t) ;; hide the startup message
(load-theme 'material t) ;; load material theme
(global-linum-mode t) ;; enable line numbers globally

;; PYTHON CONFIGURATION
;; --------------------------------------

;; use flycheck not flymake with elpy
(when (require 'flycheck nil t)
  (setq elpy-modules (delq 'elpy-module-flymake elpy-modules))
  (add-hook 'elpy-mode-hook 'flycheck-mode))


;;Permet d'utiliser les fleches dans le shell d'emacs
(progn(require 'comint)
      (define-key comint-mode-map (kbd "<up>") 'comint-previous-input)
      (define-key comint-mode-map (kbd "<down>" ) 'comint-next-input))
