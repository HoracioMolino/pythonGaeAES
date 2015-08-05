#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template
import os
from Crypto.PublicKey import RSA

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )


def getSavedKey():
    kpath = os.path.join(os.path.dirname(__file__), 'key.txt')
    fi = open(kpath,'r')
    kes = fi.read()
    return RSA.importKey(kes)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        newKS = getSavedKey()
        modulus  = hex(newKS.publickey().n)[2:-1]
        exponent = hex(newKS.publickey().e)[2:-1]
        templateValues = {'modulus':modulus, 'exponent':exponent}
        fpath = os.path.join(os.path.dirname(__file__),'forms/main.html')
        frm = template.render(fpath, templateValues)
        self.response.out.write(frm)

    def post(self):
        cEnc = self.request.get('encrypted')
        chEnc = HexToByte(cEnc)
        k = getSavedKey()
        cDec = k.decrypt(chEnc)
        self.response.out.write(cDec)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
