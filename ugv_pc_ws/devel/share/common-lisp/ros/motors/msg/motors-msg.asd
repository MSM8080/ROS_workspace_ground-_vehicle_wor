
(cl:in-package :asdf)

(defsystem "motors-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "arduino_motors" :depends-on ("_package_arduino_motors"))
    (:file "_package_arduino_motors" :depends-on ("_package"))
  ))