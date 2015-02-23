data='''
Stmt([Function(None, 'factorial', ('n',), (), 0, None, Stmt([If([(Compare(Name('n'), [('<', Const(2))]), Stmt([Return(Const(1))]))], None), Return(Mul((Name('n'), CallFunc(Name('factorial'), [Sub((Name('n'), Const(1)))], None, None))))])), Print(CallFunc(Name('factorial'), [Const(5)], None, None), None)])'''
output="""
Stmt(
		[
			Function
				(
					None, 'factorial', ('n',), (), 0, None, Stmt(
																	[
																		If(
																			[
																				(Compare
																					(Name('n'), [('<', Const(2))]
																					), 
																					Stmt([Return(Const(1))])
																				)
																			],
																			None
																		  ), 
																		Return(
																				Mul(
																					(
																						Name('n'), 
																						CallFunc
																						(
																							Name('factorial'), 
																							[Sub((Name('n'), Const(1)))], 
																							None, None
																						)
																					)
																				   )
																			  )
																	]
															 	)
				), 
			
			Print(
					CallFunc(
								Name('factorial'), [Const(5)], None, None
							), 
					None
				)
		]
	)
"""
