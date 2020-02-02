
import base64
import binascii


class ApiUtil:

    @staticmethod
    def is_base64(str_b64):
        """Check if str represents base64 format.
        Args:
            str_b64 (str): String containing base64 code.
        Returns:
            bool: True if input is base64 encoded, raise ValueError otherwise.
        Raises:
            ValueError: Wrong base64 input.
        """
        try:
            base64.b64decode(str_b64)
        except binascii.Error:
            raise ValueError('No correct base64 value.')
        return True
