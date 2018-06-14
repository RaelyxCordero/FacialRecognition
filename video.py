#!/usr/bin/env python
import os
import cv2
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
import pickle
import numpy as np
import MySQLdb

db = MySQLdb.connect(host="localhost",      # your host, usually localhost
                     user="root",           # your username
                     passwd="123",          # your password
                     db="neuraltest")       # name of the data base


class UsbCamera(object):

    """ Init camera """
    def __init__(self):
        # select first video device in system
        self.cam = cv2.VideoCapture(-1)
        self.detect = False
        self.name = ''
        # set camera resolution
        self.w = 320
        self.h = 240
        self.cant_train = 5
        self.cant_test = 3
        self.cant_total = self.cant_train + self.cant_test
        self.n_comp = 50
        # set crop factor
        self.cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.h)
        self.cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.w)
        # load cascade file
        self.face_cascade = cv2.CascadeClassifier('face.xml')
    def checkCam(self):
        if self.cam.isOpened():
            return True
        else:
            return False

    def restart(self):
        self.cam.open(-1)

    def close_cam(self):
        if self.checkCam():
            self.cam.release()
            self.reset = True

    def set_resolution(self, new_w, new_h):
        """
        functionality: Change camera resolution
        inputs: new_w, new_h - with and height of picture, must be int
        returns: None ore raise exception
        """
        if isinstance(new_h, int) and isinstance(new_w, int):
            # check if args are int and correct
            if (new_w <= 800) and (new_h <= 600) and \
               (new_w > 0) and (new_h > 0):
                self.h = new_h
                self.w = new_w
            else:
                # bad params
                raise Exception('Bad resolution')
        else:
            # bad params
            raise Exception('Not int value')

    def predictNN(self, data):
        # load the model from disk
        cur = db.cursor()
        
        loaded_model = pickle.load(open('./finalized_model.sav', 'rb'))
        prob = loaded_model.predict_proba(data)
        prediction = loaded_model.predict(data)
        score = loaded_model.score(data, [364])
        print("score: %s \n" % score)
        print np.amax(prob)*100.00
        print prediction
        sql = "SELECT name FROM users WHERE id = %s;"
        # cur.execute("""SELECT name FROM users WHERE id = %s""", (prediction[0],))
        cur.execute("""SELECT name FROM users WHERE id = %s""", (prediction[0],))
        data=cur.fetchone()

        # 
        # print("prediccion: %s \n" % data[0])
        # if prob[0][0]*100 > 60:
        return data[0], prediction[0]

    def testProcess(self, model):
        test_data = np.load('./test_data.npy')
        outtest_data = np.load('./outtest_data.npy')
        print("Test set score: %f" % model.score(test_data, outtest_data))
        print("Prob score:")
        print model.predict_proba(test_data)

    def trainNN(self, training_data, output_data):
        e1 = cv2.getTickCount()
        print "Building Perceptron..."
        #Creating MultiLayer Perceptrons.
        mlp = MLPClassifier(hidden_layer_sizes=(32,16),activation='logistic',solver='sgd',
                            learning_rate_init=0.1, alpha=0.1,
                            random_state=1, max_iter=20000, 
                            momentum=0)
        mlp.out_activation_ = 'identity'

        print "Training MLP............."
        mlp.fit(training_data, output_data)
        e2 = cv2.getTickCount()
        time_taken = (e2-e1)/cv2.getTickFrequency()
        print "Time taken to train : ", time_taken
        print mlp.get_params()
        # print("Training set score: %f" % mlp.score(training_data, output_data))
        # print("Test set score: %f" % mlp.score(training_data[0].reshape(1,-1), output_data[0].reshape(1,-1)))
        # print mlp.predict(training_data[3].reshape(1,-1))
        # self.testProcess(mlp)
        # save the model to disk
        filename = 'finalized_model.sav'
        pickle.dump(mlp, open(filename, 'wb'))

    def picHandler(self):
        if self.detect:
            encode = [int(cv2.IMWRITE_JPEG_QUALITY), 150]
            result, imgencode = cv2.imencode('.jpg', self.image, encode)
            data = np.array(imgencode)
            decimg = cv2.imdecode(data, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            sub_face = decimg[self.b:self.b+self.d, self.a:self.a+self.c]
            dim = (50 , 50)
            sub_face = cv2.resize(sub_face, dim, interpolation = cv2.INTER_AREA)
            # FaceFileName = "face_prueba.jpg"
            # cv2.imwrite(FaceFileName, sub_face)
            pca = PCA(self.n_comp)
            pca.fit(sub_face)
            img_gray_pca = pca.fit_transform(sub_face)
            img_array = np.zeros((1, 0))

            for comp in img_gray_pca:
                img_array = np.hstack((img_array, comp[None,:]))
            return img_array

    def ident_pic(self):
        self.name = ''
        if not self.detect:
            return self.name, 0
        img_gray_pca = self.picHandler()
        img_array = np.zeros((1, 0))

        for comp in img_gray_pca:
            img_array = np.hstack((img_array, comp[None,:]))

        self.name, uid = self.predictNN(img_array.reshape(1,-1))
        return self.name, uid

    def train_pic(self, uid, qty):
        if not self.detect:
            return False

        uid = int(uid)
        qty = int(qty)

        img_gray_pca = self.picHandler()
        # Adjust Array Matrix
        training_temp = np.zeros((1, 0))
        for comp in img_gray_pca:
            training_temp = np.hstack((training_temp, comp[None,:]))
        # print training_temp.shape
        if 'training_data' in locals():
            training_data = np.vstack((training_data, training_temp))
        else:
            training_data = training_temp
        if qty <= self.cant_train:
            # Load & save NPArray
            if os.path.isfile('./training_data.npy') and os.path.isfile('./output_data.npy'):
                # training data
                all_training_data = np.load('./training_data.npy')
                training_data = np.vstack((all_training_data, training_data))
                print 'Shape of training_data: '
                print training_data.shape
                np.save('training_data.npy', training_data)
                # output data
                output_data = np.load('./output_data.npy')
                out = np.full((1,1),uid).reshape(1,1)
                output_data = np.vstack((output_data, out))
                np.save('output_data.npy', output_data)
                print 'Shape of output_data: '
                print output_data.shape
                print output_data
            else:
                # training data
                np.save('training_data.npy', training_data)
                print 'Shape of training_data: '
                print training_data.shape
                # output data
                output_data = np.full((1,1),uid).reshape(1,1)
                print 'Shape of output_data: '
                print output_data.shape
                print output_data
                np.save('output_data.npy', output_data)
            if qty == self.cant_train - 1:
                ended_training_data = training_data
                print ended_training_data.shape
                
        if qty == self.cant_train -1:
            # NEURAL NETWORK STEP FOR TRAINING
            print 'VOY A ENTRENAAAAR'
            self.trainNN(ended_training_data, output_data)
        return True

    def get_frame(self, fdenable):
        """
        functionality: Gets frame from camera and try to find feces on it
        :return: byte array of jpeg encoded camera frame
        """
        self.detect = False
        success, self.image = self.cam.read()
        if success:
            # scale image
            self.image = cv2.resize(self.image, (self.w, self.h))
            if fdenable:
                # resize image for speeding up recognize
                gray = cv2.resize(self.image, (320, 240))
                # make it grayscale
                gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
                # face cascade detector
                faces = self.face_cascade.detectMultiScale(gray)
                # draw rect on face arias
                scale = float(self.w / 320.0)
                count = 0
                for f in faces:
                    self.detect = True
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    x, y, w, h = [int(float(v) * scale) for v in f]
                    if self.name:
                        cv2.putText(self.image, self.name, (x,y), font, 1, (255, 255, 255),1)
                    # cv2.putText(image, str(x) + ' ' + str(y), (0, (self.h - 10 - 25 * count)), font, 1, (0, 0, 0), 2)
                    count += 1
                    cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    (self.a, self.b, self.c, self.d) = (x,y,w,h)
        else:
            self.image = np.zeros((self.h, self.w, 3), np.uint8)
            cv2.putText(self.image, 'No camera', (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        # encoding picture to jpeg
        ret, jpeg = cv2.imencode('.jpg', self.image)
        return jpeg.tostring()
