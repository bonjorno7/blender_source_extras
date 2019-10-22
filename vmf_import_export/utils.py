from .datatypes import *


class brush_utils:

    @staticmethod
    def get_normal(v1, v2 = None, v3 = None):
        if v2 is not None and v3 is not None:

            return -vec3.cross(v2-v1, v3-v1).n()
        else:
            return -vec3.cross(v1.v2-v1.v1, v1.v3-v1.v1).n()

    @staticmethod
    def get_dist_to_origin(v1,v2=None,v3=None, is_normal=False):
        if is_normal is False:
            n=None
            q=None
            if v2 is not None and v3 is not None:
                n = brush_utils.get_normal(v1,v2,v3)
                q = v1
            else:
                n = brush_utils.get_normal(v1)
                q = v1.v1
        else:
            n = v1
            q = v2
        return -vec3.dot(n,q)
            

    @staticmethod
    def get_intersection(v1, v2, v3):
        n1 = v1.normal    
        n2 = v2.normal
        n3 = v3.normal

        d1 = v1.d
        d2 = v2.d
        d3 = v3.d


        denom = vec3.dot(n1, vec3.cross(n2,n3))

        if abs(denom) < 10**-8:
            return None


        ret = ( ((vec3.cross(n2,n3)) * (d1))
               +((vec3.cross(n3,n1)) * (d2))
               +((vec3.cross(n1,n2)) * (d3))) / -denom
        return ret

if __name__ == "__main__":
    print(brush_utils.get_intersection(
        vec3x3("(-1492 1144 736) (-1492 1144 -352) (7560 1144 -352)"),
        vec3x3("(7560 1144 736) (7560 1144 -352) (7560 1136 -352)"),
        vec3x3("(7560 1144 -352) (-1492 1144 -352) (-1492 1136 -352)")
        ).string())
        
