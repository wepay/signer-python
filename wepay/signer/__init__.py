# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2016 WePay.

Based on a stripped-down version of the AWS Signature v4 implementation.

http://opensource.org/licenses/Apache2.0
"""

from __future__ import print_function
import hashlib
import hmac
import six

class Signer:
    """
    The Signer class is designed for those who are signing data on behalf of a public-private keypair.

    In principle, the "client party" has public key (i.e., `client_id`) has a matching private key
    (i.e., `client_secret`) that can be verified by both the signer, as well as the client, but
    by nobody else as we don't want to make forgeries possible.

    The "signing party" has a simple an identifier which acts as an additional piece of entropy in the
    algorithm, and can help differentiate between multiple signing parties if the client party does
    something like try to use the same public-private keypair independently of a signing party
    (as is common with GPG signing).

    For example, in the original AWS implementation, the "self key" for AWS was "AWS4".
    """

    def __init__(self, client_id, client_secret, options = {}):
        """
        Constructs a new instance of this class.

        @param client_id [String] A string which is the public portion of the keypair identifying the client party. The
            pairing of the public and private portions of the keypair should only be known to the client party and the
            signing party.
        @param client_secret [String] A string which is the private portion of the keypair identifying the client party.
            The pairing of the public and private portions of the keypair should only be known to the client party and
            the signing party.
        @option options [String] self_key (WePay) A string which identifies the signing party and adds additional entropy.
        @option options [String] hash_algo (sha512) The hash algorithm to use for signing.
        """

        self.client_id = "{client_id}".format(client_id=client_id)
        self.client_secret = "{client_secret}".format(client_secret=client_secret)

        merged_options = options.copy()
        merged_options.update({
            "self_key":  "WePay",
            "hash_algo": hashlib.sha512,
        })

        self.self_key  = merged_options["self_key"]
        self.hash_algo = merged_options["hash_algo"]

    def sign(self, payload):
        """
        Sign the payload to produce a signature for its contents.

        @param payload [Hash] The data to generate a signature for.
        @option payload [required, String] token The one-time-use token.
        @option payload [required, String] page The WePay URL to access.
        @option payload [required, String] redirect_uri The partner URL to return to once the action is completed.
        @return [String] The signature for the payload contents.
        """

        merged_payload = payload.copy()
        merged_payload.update({
            'client_id':     self.client_id,
            'client_secret': self.client_secret,
        })

        scope = self.__create_scope()
        context = self.__create_context(merged_payload)
        s2s = self.__create_string_to_sign(scope, context)
        signing_key = self.__get_signing_salt()

        signature = hmac.new(
            signing_key,
            six.u(s2s).encode('utf-8'),
            self.hash_algo
        ).hexdigest()

        return signature

    def generate_query_string_params(self, payload):
        """
        Signs and generates the query string URL parameters to use when making a request.

        If the `client_secret` key is provided, then it will be automatically excluded from the result.

        @param  payload [Hash] The data to generate a signature for.
        @option payload [required, String] token The one-time-use token.
        @option payload [required, String] page The WePay URL to access.
        @option payload [required, String] redirect_uri The partner URL to return to once the action is completed.
        @return [String] The query string parameters to append to the end of a URL.
        """

        payload.pop('client_secret', None)

        signed_token = self.sign(payload)
        payload['client_id'] = self.client_id
        payload['stoken'] = signed_token
        qsa = []

        payload_keys = list(six.viewkeys(payload))
        payload_keys.sort()

        for key in payload_keys:
            qsa.append("{}={}".format(key, payload[key]))

        return "&".join(qsa)


    # --------------------------------------------------------------------------
    # Private

    def __create_string_to_sign(self, scope, context):
        """
        Creates the string-to-sign based on a variety of factors.

        @param scope [String] The results of a call to the `__create_scope()` method.
        @param context [String] The results of a call to the `__create_context()` method.
        @return [String] The final string to be signed.
        """

        scope_hash = hashlib.new(self.hash_algo().name, scope.encode('utf-8')).hexdigest()
        context_hash = hashlib.new(self.hash_algo().name, context.encode('utf-8')).hexdigest()

        return "SIGNER-HMAC-{hash_algo}\n{self_key}\n{client_id}\n{scope_hash}\n{context_hash}".format(
            hash_algo=self.hash_algo().name.upper(),
            self_key=self.self_key,
            client_id=self.client_id,
            scope_hash=scope_hash,
            context_hash=context_hash
        )

    def __create_context(self, payload):
        """
        An array of key-value pairs representing the data that you want to sign.
        All values must be `scalar`.

        @param  payload [Hash] The data that you want to sign.
        @option payload [String] self_key (WePay) A string which identifies the signing party and adds additional entropy.
        @return [String] A canonical string representation of the data to sign.
        """

        canonical_payload = []

        for k in six.viewkeys(payload):
            val = "{}".format(payload[k]).lower()
            key = "{}".format(k).lower()
            canonical_payload.append("{}={}\n".format(key, val))

        canonical_payload.sort()

        sorted_keys = list(six.viewkeys(payload))
        sorted_keys.sort()

        signed_headers_string    = ";".join(sorted_keys)
        canonical_payload_string = "".join(canonical_payload) + "\n" + signed_headers_string

        return canonical_payload_string

    def __get_signing_salt(self):
        """
        Gets the salt value that should be used for signing.

        @return [String] The signing salt.
        """

        self_key_sign = hmac.new(
            six.b(self.client_secret),
            six.u(self.self_key).encode('utf-8'),
            self.hash_algo
        ).digest()

        client_id_sign = hmac.new(
            self_key_sign,
            six.u(self.client_id).encode('utf-8'),
            self.hash_algo
        ).digest()

        signer_sign = hmac.new(
            client_id_sign,
            six.u('signer').encode('utf-8'),
            self.hash_algo
        ).digest()

        return signer_sign

    def __create_scope(self):
        """
        Creates the "scope" in which the signature is valid.

        @return [String] The string which represents the scope in which the signature is valid.
        """

        return "{self_key}/{client_id}/signer".format(
            self_key=self.self_key,
            client_id=self.client_id
        )
