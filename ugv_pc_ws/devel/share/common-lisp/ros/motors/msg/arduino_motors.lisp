; Auto-generated. Do not edit!


(cl:in-package motors-msg)


;//! \htmlinclude arduino_motors.msg.html

(cl:defclass <arduino_motors> (roslisp-msg-protocol:ros-message)
  ((speed
    :reader speed
    :initarg :speed
    :type cl:fixnum
    :initform 0)
   (direction
    :reader direction
    :initarg :direction
    :type cl:string
    :initform ""))
)

(cl:defclass arduino_motors (<arduino_motors>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <arduino_motors>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'arduino_motors)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motors-msg:<arduino_motors> is deprecated: use motors-msg:arduino_motors instead.")))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <arduino_motors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motors-msg:speed-val is deprecated.  Use motors-msg:speed instead.")
  (speed m))

(cl:ensure-generic-function 'direction-val :lambda-list '(m))
(cl:defmethod direction-val ((m <arduino_motors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motors-msg:direction-val is deprecated.  Use motors-msg:direction instead.")
  (direction m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <arduino_motors>) ostream)
  "Serializes a message object of type '<arduino_motors>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'speed)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'direction))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'direction))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <arduino_motors>) istream)
  "Deserializes a message object of type '<arduino_motors>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'speed)) (cl:read-byte istream))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'direction) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'direction) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<arduino_motors>)))
  "Returns string type for a message object of type '<arduino_motors>"
  "motors/arduino_motors")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'arduino_motors)))
  "Returns string type for a message object of type 'arduino_motors"
  "motors/arduino_motors")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<arduino_motors>)))
  "Returns md5sum for a message object of type '<arduino_motors>"
  "57336acb67f0c9d5b2d2f2054be77759")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'arduino_motors)))
  "Returns md5sum for a message object of type 'arduino_motors"
  "57336acb67f0c9d5b2d2f2054be77759")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<arduino_motors>)))
  "Returns full string definition for message of type '<arduino_motors>"
  (cl:format cl:nil "uint8 speed~%string direction~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'arduino_motors)))
  "Returns full string definition for message of type 'arduino_motors"
  (cl:format cl:nil "uint8 speed~%string direction~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <arduino_motors>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'direction))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <arduino_motors>))
  "Converts a ROS message object to a list"
  (cl:list 'arduino_motors
    (cl:cons ':speed (speed msg))
    (cl:cons ':direction (direction msg))
))
