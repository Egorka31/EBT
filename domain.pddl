(define (domain doors)
  (:predicates (at-room ?o ?r))

  (:action deliverAB
   :parameters ()
   :expansion (series (come-to-a) (take) (come-to-b)))

  (:action come-to-a
  :parameters ()
  :expansion (series (navigate) (go)))

  (:action navigate
  :parameters ())

  (:action go
  :parameters ())

  (:action take
  :parameters ())

  (:action come-to-b
  :parameters ()
  :expansion (series (navigate) (go)))
 )
