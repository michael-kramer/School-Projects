test = {
  'name': 'Question 13',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define (f) False)
          f
          scm> (if (f) 1 0)
          0
          scm> (if f 1 0)
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (if True 1 0)
          1
          scm> (if False 1 0)
          0
          scm> (if 1 1 0)
          1
          scm> (if 0 1 0)
          1
          scm> (if 'a 1 0)
          1
          scm> (if (cons 1 2) 1 0)
          1
          scm> (if True 1)
          1
          scm> (if False 1)
          567dc50b5f172929c23f03f6621d0d6b
          # locked
          scm> (eval (if False 1))
          567dc50b5f172929c23f03f6621d0d6b
          # locked
          scm> (if True '(1))
          9f90814c29b45aacdbe10436cf085857
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    }
  ]
}