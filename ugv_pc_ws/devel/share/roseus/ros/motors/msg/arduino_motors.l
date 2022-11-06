;; Auto-generated. Do not edit!


(when (boundp 'motors::arduino_motors)
  (if (not (find-package "MOTORS"))
    (make-package "MOTORS"))
  (shadow 'arduino_motors (find-package "MOTORS")))
(unless (find-package "MOTORS::ARDUINO_MOTORS")
  (make-package "MOTORS::ARDUINO_MOTORS"))

(in-package "ROS")
;;//! \htmlinclude arduino_motors.msg.html


(defclass motors::arduino_motors
  :super ros::object
  :slots (_speed _direction ))

(defmethod motors::arduino_motors
  (:init
   (&key
    ((:speed __speed) 0)
    ((:direction __direction) "")
    )
   (send-super :init)
   (setq _speed (round __speed))
   (setq _direction (string __direction))
   self)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:direction
   (&optional __direction)
   (if __direction (setq _direction __direction)) _direction)
  (:serialization-length
   ()
   (+
    ;; uint8 _speed
    1
    ;; string _direction
    4 (length _direction)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _speed
       (write-byte _speed s)
     ;; string _direction
       (write-long (length _direction) s) (princ _direction s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _speed
     (setq _speed (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; string _direction
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _direction (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get motors::arduino_motors :md5sum-) "57336acb67f0c9d5b2d2f2054be77759")
(setf (get motors::arduino_motors :datatype-) "motors/arduino_motors")
(setf (get motors::arduino_motors :definition-)
      "uint8 speed
string direction

")



(provide :motors/arduino_motors "57336acb67f0c9d5b2d2f2054be77759")


