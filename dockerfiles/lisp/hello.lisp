(defun main ()
  (format t "Hello, world!~%"))
(sb-ext:save-lisp-and-die "hello-world"
  :executable t
  :toplevel 'main)
